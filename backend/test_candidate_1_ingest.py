import logging
sys_log = logging.getLogger()
sys_log.setLevel(logging.INFO)

from app.embeddings.embedding_service import EmbeddingService
from app.services.pipeline_service import ingest_candidate_s3_transcripts
from app.vectorstore.chroma_service import ChromaService

def test_ingest_user_1():
    print("--- Testing Ingestion for user_id='1' ---", flush=True)
    emb_svc = EmbeddingService()
    chroma_svc = ChromaService()
    
    res = ingest_candidate_s3_transcripts(
        user_id="1",
        limit=1,
        embedding_service=emb_svc,
        chroma_service=chroma_svc,
    )
    print(f"Result: {res}", flush=True)

if __name__ == "__main__":
    test_ingest_user_1()
