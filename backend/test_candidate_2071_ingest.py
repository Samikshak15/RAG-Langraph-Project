from app.embeddings.embedding_service import EmbeddingService
from app.services.pipeline_service import ingest_candidate_s3_transcripts
from app.vectorstore.chroma_service import ChromaService

def test_ingest_user_2071():
    print("--- Testing Ingestion for user_id='2071' ---", flush=True)
    emb_svc = EmbeddingService()
    chroma_svc = ChromaService()
    
    res = ingest_candidate_s3_transcripts(
        user_id="2071",
        limit=1,
        embedding_service=emb_svc,
        chroma_service=chroma_svc,
    )
    print(f"Result: {res}", flush=True)

if __name__ == "__main__":
    test_ingest_user_2071()
