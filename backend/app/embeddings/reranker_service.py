import threading

from sentence_transformers import CrossEncoder

from app.config import RERANK_MODEL_NAME


class RerankerService:
    """Wraps CrossEncoder.predict(). The model itself is loaded lazily on
    first .score() call (not at construction) — this box has repeatedly
    struggled to keep one sentence-transformers model resident; deferring
    the second one avoids paying its cost for requests that never search."""

    def __init__(self):
        self._model: CrossEncoder | None = None
        self._lock = threading.Lock()

    def _ensure_loaded(self) -> CrossEncoder:
        if self._model is None:
            with self._lock:
                if self._model is None:
                    self._model = CrossEncoder(RERANK_MODEL_NAME)
        return self._model

    def score(self, query: str, texts: list[str]) -> list[float]:
        if not texts:
            return []
        model = self._ensure_loaded()
        return model.predict([(query, text) for text in texts]).tolist()
