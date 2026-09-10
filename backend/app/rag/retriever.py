import json

from app.config import RERANK_CANDIDATE_CEILING, RERANK_CANDIDATE_MULTIPLIER
from app.embeddings.embedding_service import EmbeddingService
from app.embeddings.reranker_service import RerankerService
from app.vectorstore.chroma_service import ChromaService


def _deserialize_list_field(value) -> list:
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return []
    return value or []


class Retriever:
    def __init__(
        self,
        embedding_service: EmbeddingService,
        chroma_service: ChromaService,
        reranker_service: RerankerService,
    ):
        self.embedding_service = embedding_service
        self.chroma_service = chroma_service
        self.reranker_service = reranker_service

    def search(self, query: str, only_scored: bool, n_results: int) -> list[dict]:
        query_embedding = self.embedding_service.embed_text(query)
        where = {"counts_toward_score": True} if only_scored else None

        candidate_n = max(
            min(n_results * RERANK_CANDIDATE_MULTIPLIER, RERANK_CANDIDATE_CEILING),
            n_results,
        )
        raw = self.chroma_service.query(query_embedding, n_results=candidate_n, where=where)

        candidates = []
        for chunk_id, text, meta, distance in zip(
            raw["ids"][0], raw["documents"][0], raw["metadatas"][0], raw["distances"][0]
        ):
            candidates.append({
                "chunk_id": chunk_id, "text": text, "distance": distance,
                "session_id": meta.get("session_id"), "user_id": meta.get("user_id"),
                "question_id": meta.get("question_id"), "question": meta.get("question"),
                "answer": meta.get("answer"), "topic": meta.get("topic"),
                "subtopic": meta.get("subtopic"), "score": meta.get("score"),
                "strengths": _deserialize_list_field(meta.get("strengths")),
                "weaknesses": _deserialize_list_field(meta.get("weaknesses")),
                "missing_concepts": _deserialize_list_field(meta.get("missing_concepts")),
                "feedback": meta.get("feedback"),
                "counts_toward_score": meta.get("counts_toward_score"),
            })

        if not candidates:
            return []

        rerank_scores = self.reranker_service.score(query, [c["text"] for c in candidates])
        for candidate, rerank_score in zip(candidates, rerank_scores):
            candidate["rerank_score"] = rerank_score

        candidates.sort(key=lambda c: c["rerank_score"], reverse=True)
        return candidates[:n_results]

    def search_candidate(self, query: str, user_id: str, only_scored: bool = False, n_results: int = 5) -> list[dict]:
        """
        Candidate-filtered RAG search: queries ChromaDB filtered by user_id and optionally counts_toward_score.
        """
        query_embedding = self.embedding_service.embed_text(query)
        
        where = {"user_id": str(user_id)}
        if only_scored:
            where = {"$and": [{"user_id": str(user_id)}, {"counts_toward_score": True}]}

        candidate_n = max(
            min(n_results * RERANK_CANDIDATE_MULTIPLIER, RERANK_CANDIDATE_CEILING),
            n_results,
        )
        raw = self.chroma_service.query(query_embedding, n_results=candidate_n, where=where)

        if not raw or not raw.get("ids") or not raw["ids"][0]:
            return []

        candidates = []
        for chunk_id, text, meta, distance in zip(
            raw["ids"][0], raw["documents"][0], raw["metadatas"][0], raw["distances"][0]
        ):
            candidates.append({
                "chunk_id": chunk_id, "text": text, "distance": distance,
                "session_id": meta.get("session_id"), "user_id": meta.get("user_id"),
                "question_id": meta.get("question_id"), "question": meta.get("question"),
                "answer": meta.get("answer"), "topic": meta.get("topic"),
                "subtopic": meta.get("subtopic"), "score": meta.get("score"),
                "strengths": _deserialize_list_field(meta.get("strengths")),
                "weaknesses": _deserialize_list_field(meta.get("weaknesses")),
                "missing_concepts": _deserialize_list_field(meta.get("missing_concepts")),
                "feedback": meta.get("feedback"),
                "counts_toward_score": meta.get("counts_toward_score"),
            })

        rerank_scores = self.reranker_service.score(query, [c["text"] for c in candidates])
        for candidate, rerank_score in zip(candidates, rerank_scores):
            candidate["rerank_score"] = rerank_score

        candidates.sort(key=lambda c: c["rerank_score"], reverse=True)
        return candidates[:n_results]

