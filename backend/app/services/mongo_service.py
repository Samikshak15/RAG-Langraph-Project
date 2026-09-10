import logging
from datetime import datetime, timezone
from typing import Any, Optional
from pymongo import MongoClient
from app.config import INTELLICONVO_DB_NAME, INTELLICONVO_URI

logger = logging.getLogger(__name__)


def _user_id_filter(user_id_input: Any) -> dict:
    """
    Construct MongoDB filter matching both NumberInt(1) and string "1".
    """
    clean_str = str(user_id_input).strip()
    if clean_str.isdigit():
        return {"$in": [int(clean_str), clean_str]}
    return clean_str


class MongoService:
    def __init__(self, uri: Optional[str] = None, db_name: Optional[str] = None):
        self.uri = uri or INTELLICONVO_URI
        self.db_name = db_name or INTELLICONVO_DB_NAME
        self.client: Optional[MongoClient] = None
        self.db = None
        self._connected = False
        self._init_connection()

    def _init_connection(self):
        try:
            # 3 second server selection timeout so offline runs fallback gracefully
            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=3000)
            self.db = self.client[self.db_name]
            # Quick ping test
            self.client.admin.command("ping")
            self._connected = True
            logger.info("Connected to IntelliConvo MongoDB '%s' at '%s'", self.db_name, self.uri)
        except Exception as exc:
            logger.warning("IntelliConvo MongoDB not available at '%s': %s (fallback active)", self.uri, exc)
            self._connected = False

    @property
    def is_connected(self) -> bool:
        return self._connected

    def find_user_id_by_name(self, name_query: str) -> Optional[str]:
        """
        Search auth_app_t_user collection (READ-ONLY) by candidate first_name, last_name, or username.
        """
        if not self.is_connected or not name_query or not name_query.strip():
            return None

        clean_name = name_query.strip()
        regex_pattern = {"$regex": f"^{clean_name}$", "$options": "i"}
        partial_pattern = {"$regex": clean_name, "$options": "i"}

        try:
            col = self.db["auth_app_t_user"]
            # Exact match first
            doc = col.find_one({
                "$or": [
                    {"first_name": regex_pattern},
                    {"last_name": regex_pattern},
                    {"username": regex_pattern},
                    {"user_email": regex_pattern},
                ]
            })
            if not doc:
                # Partial substring match fallback
                doc = col.find_one({
                    "$or": [
                        {"first_name": partial_pattern},
                        {"last_name": partial_pattern},
                        {"username": partial_pattern},
                        {"user_email": partial_pattern},
                    ]
                })

            if doc and doc.get("user_id") is not None:
                uid = str(doc["user_id"])
                logger.info("Found MongoDB candidate record for '%s' -> user_id: %s", clean_name, uid)
                return uid
        except Exception as exc:
            logger.error("Error querying auth_app_t_user in MongoDB: %s", exc)

        return None

    def get_candidate_sessions(self, user_id: str, limit: int = 3) -> list[dict]:
        """
        Query auth_app_t_request collection (READ-ONLY) for completed interview sessions of user_id.
        Supports both integer (NumberInt) and string user_ids.
        """
        if not self.is_connected or not user_id:
            return []

        try:
            col = self.db["auth_app_t_request"]
            uid_query = _user_id_filter(user_id)
            cursor = col.find({
                "user_id": uid_query,
                "process_status": {"$regex": "Process Completed|Completed", "$options": "i"},
            }).sort("created_at", -1).limit(limit)

            sessions = []
            for doc in cursor:
                session_id = str(doc.get("session_id", ""))
                bot_id = str(doc.get("bot_id", "358"))
                s3_key = f"simulation_training/{user_id}/{bot_id}/{session_id}/{session_id}_transcript.txt"

                sessions.append({
                    "session_id": session_id,
                    "user_id": str(user_id),
                    "bot_id": bot_id,
                    "source_key": s3_key,
                    "process_status": doc.get("process_status"),
                    "overall_ai_score": doc.get("average_maximum_score"),
                    "session_start_time": str(doc.get("created_at", "")),
                })
            return sessions
        except Exception as exc:
            logger.error("Error querying auth_app_t_request in MongoDB: %s", exc)
            return []

    def list_all_users_from_mongo(self, limit: int = 2000, search: Optional[str] = None) -> list[dict]:
        """
        Fetch candidate records (READ-ONLY) from MongoDB auth_app_t_user collection.
        Supports fetching up to 2000+ candidates or filtering by name search.
        """
        if not self.is_connected:
            return []
        try:
            col = self.db["auth_app_t_user"]
            query_filter = {}
            if search and search.strip():
                clean_s = search.strip()
                p = {"$regex": clean_s, "$options": "i"}
                query_filter = {"$or": [{"first_name": p}, {"last_name": p}, {"username": p}, {"user_email": p}]}

            cursor = col.find(
                query_filter,
                {"user_id": 1, "first_name": 1, "last_name": 1, "user_email": 1, "username": 1}
            )
            if limit and limit > 0:
                cursor = cursor.limit(limit)

            candidates = []
            for doc in cursor:
                fn = str(doc.get("first_name") or "").strip()
                ln = str(doc.get("last_name") or "").strip()
                full_name = f"{fn} {ln}".strip() or doc.get("username") or doc.get("user_email") or f"User {doc.get('user_id')}"
                candidates.append({
                    "user_id": str(doc.get("user_id")),
                    "name": full_name,
                    "email": doc.get("user_email"),
                    "source": "mongo_db",
                })
            return candidates
        except Exception as exc:
            logger.error("Error listing users from MongoDB auth_app_t_user: %s", exc)
            return []

    # -------------------------------------------------------------------------
    # Project-Specific Storage Collection: rag_candidate_reports
    # (Keeps IntelliConvo collections completely untouched)
    # -------------------------------------------------------------------------

    def save_candidate_report(self, report_dict: dict[str, Any]) -> Optional[str]:
        """
        Saves a generated multi-interview performance report in dedicated rag_candidate_reports collection.
        """
        if not self.is_connected:
            return None
        try:
            col = self.db["rag_candidate_reports"]
            payload = dict(report_dict)
            payload["saved_at"] = datetime.now(timezone.utc).isoformat()
            res = col.insert_one(payload)
            logger.info("Saved RAG candidate report to rag_candidate_reports (id: %s)", res.inserted_id)
            return str(res.inserted_id)
        except Exception as exc:
            logger.error("Failed to save report to rag_candidate_reports: %s", exc)
            return None

    def get_saved_reports(self, user_id: str, limit: int = 5) -> list[dict]:
        """
        Retrieves historical performance reports saved for a user_id from rag_candidate_reports.
        """
        if not self.is_connected or not user_id:
            return []
        try:
            col = self.db["rag_candidate_reports"]
            cursor = col.find({"user_id": str(user_id)}).sort("saved_at", -1).limit(limit)
            reports = []
            for doc in cursor:
                doc["_id"] = str(doc["_id"])
                reports.append(doc)
            return reports
        except Exception as exc:
            logger.error("Failed to fetch saved reports from rag_candidate_reports: %s", exc)
            return []
