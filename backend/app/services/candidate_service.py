import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

from app.config import CANDIDATES_PATH
from app.ingestion.metadata_extractor import (
    extract_s3_metadata,
    extract_session_start_time,
)
from app.services.s3_service import S3Service

logger = logging.getLogger(__name__)


class CandidateService:
    def __init__(self, s3_service: Optional[S3Service] = None, registry_path: Optional[str | Path] = None):
        self._s3_service = s3_service
        self.registry_path = Path(registry_path or CANDIDATES_PATH)
        self.candidates: list[dict] = []
        self._load_registry()

    @property
    def s3_service(self) -> S3Service:
        if self._s3_service is None:
            self._s3_service = S3Service()
        return self._s3_service

    def _load_registry(self) -> None:
        """Load candidate name <-> user_id registry from JSON if exists."""
        if self.registry_path.exists():
            try:
                with open(self.registry_path, "r", encoding="utf-8") as f:
                    self.candidates = json.load(f)
                logger.info("Loaded %d candidate(s) from registry %s", len(self.candidates), self.registry_path)
            except Exception as exc:
                logger.error("Failed to load candidates registry: %s", exc)
                self.candidates = []
    def register_candidate(self, user_id: str, name: str, email: Optional[str] = None) -> dict:
        """Register a new candidate mapping name <-> user_id and save to candidates.json."""
        new_entry = {"user_id": str(user_id), "name": name.strip(), "email": email}
        # Replace if exists
        self.candidates = [c for c in self.candidates if c.get("user_id") != str(user_id)]
        self.candidates.append(new_entry)
        try:
            with open(self.registry_path, "w", encoding="utf-8") as f:
                json.dump(self.candidates, f, indent=2)
            logger.info("Registered candidate '%s' (user_id=%s)", name, user_id)
        except Exception as exc:
            logger.error("Failed to save candidates registry: %s", exc)
        return new_entry

    def resolve_user_id(self, query_or_name: str) -> Optional[str]:
        """
        Find user_id given a candidate name or user_id string.
        1. If numeric (e.g. "2071"), return directly.
        2. Query IntelliConvo MongoDB auth_app_t_user if connected.
        3. Fallback to candidates.json registry file.
        """
        clean_query = query_or_name.strip()
        if not clean_query:
            return None

        if clean_query.isdigit():
            return clean_query

        # 2. Query MongoDB auth_app_t_user
        try:
            from app.services.mongo_service import MongoService
            mongo_service = MongoService()
            if mongo_service.is_connected:
                mongo_user_id = mongo_service.find_user_id_by_name(clean_query)
                if mongo_user_id:
                    return mongo_user_id
        except Exception as exc:
            logger.warning("MongoDB lookup skipped: %s", exc)

        # 3. Fallback to local candidates.json
        for candidate in self.candidates:
            if candidate.get("name", "").lower() == clean_query.lower():
                return candidate["user_id"]

        for candidate in self.candidates:
            if clean_query.lower() in candidate.get("name", "").lower():
                return candidate["user_id"]

        return None

    def get_candidate_sessions(self, user_id: str, limit: int = 3) -> list[dict]:
        """
        Fetch sessions for a given user_id directly from S3 using prefix isolation.
        
        S3 Prefix: simulation_training/{user_id}/
        Returns list of sorted session dictionaries (newest first).
        """
        prefix = f"simulation_training/{user_id}/"
        logger.info("Fetching candidate sessions for user_id '%s' with prefix '%s'", user_id, prefix)
        
        objects = self.s3_service.list_objects(prefix=prefix)
        transcripts = [o for o in objects if o["Key"].endswith("_transcript.txt")]

        session_list = []
        for obj in transcripts:
            key = obj["Key"]
            try:
                meta = extract_s3_metadata(key)
                raw_bytes = self.s3_service.get_object(key)
                raw_text = raw_bytes.decode("utf-8", errors="ignore")
                start_time = extract_session_start_time(raw_text)

                last_mod = obj.get("LastModified")
                effective_time = start_time or (last_mod.isoformat() if hasattr(last_mod, "isoformat") else str(last_mod))

                meta["session_start_time"] = effective_time
                meta["raw_text"] = raw_text
                meta["file_size_bytes"] = obj.get("Size", len(raw_bytes))
                session_list.append(meta)
            except Exception as exc:
                logger.warning("Error processing transcript S3 key '%s': %s", key, exc)

        # Sort chronologically (newest first)
        def parse_time(val):
            if isinstance(val, datetime):
                return val
            if isinstance(val, str):
                try:
                    return datetime.fromisoformat(val)
                except ValueError:
                    pass
            return datetime.min

        session_list.sort(key=lambda s: parse_time(s.get("session_start_time")), reverse=True)
        return session_list[:limit]

    def discover_candidates_from_s3(self) -> list[dict]:
        """
        Auto-discover all user_ids present in S3 bucket under simulation_training/.
        Returns list of candidate dictionaries.
        """
        logger.info("Auto-discovering candidate user_ids from S3...")
        objects = self.s3_service.list_objects(prefix="simulation_training/")
        
        user_map: dict[str, int] = {}
        for obj in objects:
            key = obj["Key"]
            parts = key.split("/")
            if len(parts) >= 2 and parts[0] == "simulation_training":
                uid = parts[1]
                if uid.isdigit():
                    user_map[uid] = user_map.get(uid, 0) + 1

        registry_map = {c["user_id"]: c.get("name") for c in self.candidates}
        
        discovered = []
        for uid, count in sorted(user_map.items()):
            name = registry_map.get(uid, f"Candidate {uid}")
            discovered.append({
                "user_id": uid,
                "name": name,
                "is_registered": uid in registry_map,
                "s3_object_count": count,
            })
            
        return discovered

    def list_candidates(self, auto_discover: bool = False, limit: int = 2000, search: Optional[str] = None) -> list[dict]:
        """
        List candidate profiles.
        Primary Source: MongoDB auth_app_t_user collection.
        Fallback Source: S3 folder discovery / local candidates.json.
        """
        try:
            from app.services.mongo_service import MongoService
            mongo_service = MongoService()
            if mongo_service.is_connected:
                mongo_users = mongo_service.list_all_users_from_mongo(limit=limit, search=search)
                if mongo_users:
                    logger.info("Retrieved %d candidate(s) directly from MongoDB auth_app_t_user", len(mongo_users))
                    return mongo_users
        except Exception as exc:
            logger.warning("MongoDB user listing skipped: %s", exc)

        if auto_discover:
            return self.discover_candidates_from_s3()

        return self.candidates


