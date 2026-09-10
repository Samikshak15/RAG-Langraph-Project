from unittest.mock import MagicMock, patch

from app.embeddings.embedding_service import EmbeddingService
from app.embeddings.reranker_service import RerankerService
from app.services.rag_qa_service import CandidateQAService
from app.vectorstore.chroma_service import ChromaService


def test_candidate_qa_service_mocked():
    """Unit test for CandidateQAService using mock LLM & mock candidate service."""
    mock_llm = MagicMock()
    mock_llm.generate.return_value = "Candidate demonstrated strong understanding of vector similarity search."

    mock_cand_svc = MagicMock()
    mock_cand_svc.resolve_user_id.return_value = "2071"
    mock_cand_svc.list_candidates.return_value = [{"user_id": "2071", "name": "Dynamic Candidate 2071"}]

    mock_emb = MagicMock()
    mock_emb.embed_text.return_value = [0.1] * 768

    mock_reranker = MagicMock()
    mock_reranker.score.side_effect = lambda q, texts: [0.95] * len(texts)

    mock_chroma = MagicMock()
    mock_chroma.collection.get.return_value = {"ids": ["chunk_1", "chunk_2"]}
    mock_chroma.query.return_value = {
        "ids": [["chunk_1"]],
        "documents": [["Candidate answered question about vector embeddings."]],
        "metadatas": [[{
            "session_id": "session_123",
            "user_id": "2071",
            "question_id": "q1",
            "question": "What is vector similarity?",
            "answer": "Vector similarity measures distance between vectors.",
            "topic": "Embeddings & vector similarity",
            "subtopic": "Embeddings",
            "score": 8,
            "strengths": ["Clear explanation"],
            "weaknesses": [],
            "missing_concepts": [],
            "feedback": "Good answer",
            "counts_toward_score": True,
        }]],
        "distances": [[0.1]],
    }

    service = CandidateQAService(
        embedding_service=mock_emb,
        chroma_service=mock_chroma,
        reranker_service=mock_reranker,
        llm_service=mock_llm,
    )
    service.candidate_service = mock_cand_svc

    result = service.answer_candidate_query(
        candidate_query="2071",
        user_query="What are the candidate's main strengths in vector search?",
        n_results=5,
    )

    assert result["candidate_name"] == "Dynamic Candidate 2071"
    assert result["user_id"] == "2071"
    assert result["sources_retrieved_count"] == 1
    assert "vector similarity" in result["answer"]
    print("[OK] test_candidate_qa_service_mocked PASSED", flush=True)


def test_candidate_qa_service_live_indexed():
    """Integration test against actual ChromaDB collection for candidate 2071."""
    mock_llm = MagicMock()
    mock_llm.generate.return_value = "Candidate 2071 answered technical questions on generative AI, text-to-SQL, and vector databases."

    service = CandidateQAService(llm_service=mock_llm)
    
    # Query candidate 2071 (indexed in Step 1)
    result = service.answer_candidate_query(
        candidate_query="2071",
        user_query="What topics did candidate discuss?",
        n_results=3,
    )

    assert result["user_id"] == "2071"
    assert result["sources_retrieved_count"] > 0
    print(f"[OK] test_candidate_qa_service_live_indexed PASSED - retrieved {result['sources_retrieved_count']} evidence chunks", flush=True)


if __name__ == "__main__":
    print("Running Candidate RAG Q&A Engine Unit & Integration Tests...", flush=True)
    test_candidate_qa_service_mocked()
    test_candidate_qa_service_live_indexed()
    print("All Candidate RAG Q&A Engine Tests Passed Successfully!", flush=True)
