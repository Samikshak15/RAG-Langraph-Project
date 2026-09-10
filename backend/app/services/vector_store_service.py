import os

from app.config import CHROMA_PERSIST_DIR
from app.vectorstore.chroma_service import ChromaService


def _dir_size_bytes(path: str) -> int:
    total = 0
    for root, _dirs, files in os.walk(path):
        for name in files:
            total += os.path.getsize(os.path.join(root, name))
    return total


def compute_stats(chroma_service: ChromaService) -> dict:
    items = chroma_service.get_all_metadatas()
    metas = [meta for _, meta in items]
    scored = [meta for meta in metas if meta.get("counts_toward_score")]
    stored_ats = [meta["stored_at"] for meta in metas if meta.get("stored_at")]

    return {
        "total_chunks": chroma_service.collection.count(),
        "distinct_sessions": len({meta["session_id"] for meta in metas if meta.get("session_id")}),
        "avg_score": round(sum(meta["score"] for meta in scored) / len(scored), 2) if scored else 0.0,
        "vector_store_bytes": _dir_size_bytes(CHROMA_PERSIST_DIR),
        "last_stored_at": max(stored_ats) if stored_ats else None,
    }


def list_chunks(chroma_service: ChromaService, limit: int, offset: int) -> dict:
    items, total = chroma_service.list_chunks(limit, offset)

    chunks = [
        {
            "chunk_id": chunk_id,
            "question_id": meta.get("question_id"),
            "session_id": meta.get("session_id"),
            "topic": meta.get("topic"),
            "subtopic": meta.get("subtopic"),
            "score": meta.get("score"),
            "counts_toward_score": meta.get("counts_toward_score"),
            "stored_at": meta.get("stored_at"),
        }
        for chunk_id, meta in items
    ]

    return {"chunks": chunks, "total": total, "limit": limit, "offset": offset}
