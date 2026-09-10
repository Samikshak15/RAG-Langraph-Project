import os
import sys
from unittest.mock import MagicMock, patch

from app.embeddings.embedding_service import EmbeddingService
from app.services.candidate_service import CandidateService
from app.services.pipeline_service import ingest_candidate_s3_transcripts, run_pipeline_for_transcript
from app.vectorstore.chroma_service import ChromaService

# Sample transcript text for testing parsing and indexing
SAMPLE_TRANSCRIPT = """
[2026-08-07T07:57:36.776114] Agent: Hello! I'm here to conduct your technical interview.
Could you explain what a vector embedding is and how similarity search works?
[2026-08-07T07:57:59.635837] User: A vector embedding is a numerical dense vector representation of data like text or audio in a high dimensional space. Similarity search computes cosine similarity between vectors.
[2026-08-07T08:00:05.591903] Agent: Great explanation. Could you elaborate on how transformer models use self-attention mechanism?
[2026-08-07T08:00:21.245887] User: Self-attention computes attention weights between all token pairs in a sequence allowing the model to capture long range dependencies.
"""

SAMPLE_S3_KEY = "simulation_training/1797/358/session_test_123/session_test_123_transcript.txt"


def get_mock_embedding_service():
    mock_emb = MagicMock()
    mock_emb.embed_batch.side_effect = lambda texts: [[0.1] * 768 for _ in texts]
    return mock_emb


def get_mock_classifier():
    mock_c = MagicMock()
    mock_c.classify.return_value = {"topic": "Embeddings & vector similarity", "subtopic": "Embeddings"}
    return mock_c


def get_mock_evaluator():
    mock_e = MagicMock()
    mock_e.evaluate.return_value = {
        "score": 8,
        "strengths": ["Clear explanation"],
        "weaknesses": [],
        "missing_concepts": [],
        "feedback": "Good answer explaining vector embeddings",
        "counts_toward_score": True,
    }
    return mock_e


def test_run_pipeline_for_transcript():
    """Test running pipeline directly on a raw transcript string."""
    embedding_svc = get_mock_embedding_service()
    chroma_svc = ChromaService()
    
    count_before = chroma_svc.collection.count()
    with patch("app.services.pipeline_service.TopicClassifier", return_value=get_mock_classifier()), \
         patch("app.services.pipeline_service.AnswerEvaluator", return_value=get_mock_evaluator()):
        result = run_pipeline_for_transcript(
            raw_text=SAMPLE_TRANSCRIPT,
            s3_key=SAMPLE_S3_KEY,
            embedding_service=embedding_svc,
            chroma_service=chroma_svc,
        )
    
    count_after = chroma_svc.collection.count()
    assert result["session_id"] == "session_test_123"
    assert result["user_id"] == "1797"
    assert result["chunks_stored"] > 0
    assert count_after > count_before
    print(f"[OK] test_run_pipeline_for_transcript PASSED - stored {result['chunks_stored']} chunks", flush=True)


def test_ingest_candidate_s3_transcripts_mocked():
    """Test batch ingestion for a candidate user_id with mocked S3 and candidate service."""
    mock_sessions = [
        {
            "user_id": "1797",
            "bot_id": "358",
            "session_id": "session_test_123",
            "source_key": SAMPLE_S3_KEY,
            "session_start_time": "2026-09-10T10:00:00",
            "raw_text": SAMPLE_TRANSCRIPT,
        }
    ]

    mock_candidate_svc = MagicMock()
    mock_candidate_svc.get_candidate_sessions.return_value = mock_sessions

    embedding_svc = get_mock_embedding_service()
    chroma_svc = ChromaService()

    with patch("app.services.pipeline_service.CandidateService", return_value=mock_candidate_svc), \
         patch("app.services.pipeline_service.TopicClassifier", return_value=get_mock_classifier()), \
         patch("app.services.pipeline_service.AnswerEvaluator", return_value=get_mock_evaluator()):
        result = ingest_candidate_s3_transcripts(
            user_id="1797",
            limit=3,
            embedding_service=embedding_svc,
            chroma_service=chroma_svc,
        )

    assert result["status"] == "success"
    assert result["user_id"] == "1797"
    assert result["sessions_found"] == 1
    assert result["sessions_processed"] == 1
    assert result["chunks_stored"] > 0
    print(f"[OK] test_ingest_candidate_s3_transcripts_mocked PASSED - result: {result}", flush=True)


if __name__ == "__main__":
    print("Running Candidate Ingestion Unit Tests...")
    test_run_pipeline_for_transcript()
    test_ingest_candidate_s3_transcripts_mocked()
    print("All Candidate Ingestion Tests Passed Successfully!")
