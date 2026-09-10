import chromadb

from app.config import CHROMA_COLLECTION_NAME, CHROMA_PERSIST_DIR


class ChromaService:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
        self.collection = self.client.get_or_create_collection(name=CHROMA_COLLECTION_NAME)

    def add_chunks(self, chunks: list[dict], embeddings: list[list[float]]) -> None:
        self.collection.upsert(
            ids=[c["chunk_id"] for c in chunks],
            embeddings=embeddings,
            documents=[c["text"] for c in chunks],
            metadatas=[c["metadata"] for c in chunks],
        )

    def query(self, query_embedding: list[float], n_results: int = 5, where: dict | None = None) -> dict:
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where,
        )

    def get_all_metadatas(self) -> list[tuple[str, dict]]:
        # metadatas only — never embeddings/documents here, this box is memory-constrained
        result = self.collection.get(include=["metadatas"])
        return list(zip(result["ids"], result["metadatas"]))

    def list_chunks(self, limit: int, offset: int) -> tuple[list[tuple[str, dict]], int]:
        # Fetches all metadata then sorts/slices in Python — fine at current scale
        # (dozens-low-thousands of chunks); would need DB-side pagination at real scale.
        all_items = self.get_all_metadatas()
        all_items.sort(key=lambda item: item[1].get("stored_at") or "", reverse=True)
        return all_items[offset:offset + limit], len(all_items)
