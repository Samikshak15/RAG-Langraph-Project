import logging
from datetime import datetime
from typing import Optional

from app.embeddings.embedding_service import EmbeddingService
from app.embeddings.reranker_service import RerankerService
from app.rag.retriever import Retriever
from app.services.candidate_service import CandidateService
from app.services.llm_service import LLMService
from app.services.mongo_service import MongoService
from app.services.pipeline_service import ingest_candidate_s3_transcripts
from app.vectorstore.chroma_service import ChromaService

logger = logging.getLogger(__name__)


class CandidateQAService:
    def __init__(
        self,
        embedding_service: Optional[EmbeddingService] = None,
        chroma_service: Optional[ChromaService] = None,
        reranker_service: Optional[RerankerService] = None,
        llm_service: Optional[LLMService] = None,
    ):
        self.embedding_service = embedding_service or EmbeddingService()
        self.chroma_service = chroma_service or ChromaService()
        self.reranker_service = reranker_service or RerankerService()
        self.llm_service = llm_service or LLMService()
        self.retriever = Retriever(
            embedding_service=self.embedding_service,
            chroma_service=self.chroma_service,
            reranker_service=self.reranker_service,
        )
        self.candidate_service = CandidateService()

    def answer_candidate_query(
        self,
        candidate_query: str,
        user_query: str,
        n_results: int = 5,
        only_scored: bool = False,
    ) -> dict:
        """
        Dynamic Natural Language RAG Q&A Engine for Candidates:
        1. Resolves candidate user_id from name or numeric ID.
        2. Auto-ingests S3 transcripts into ChromaDB if candidate has 0 indexed vector chunks.
        3. Performs candidate-isolated RAG retrieval + cross-encoder reranking.
        4. Synthesizes grounded natural language answer using LLMService.
        5. Saves historical query report into MongoDB collection 'rag_candidate_reports'.
        """
        clean_cand = candidate_query.strip()
        user_id = self.candidate_service.resolve_user_id(clean_cand)

        if not user_id:
            known_candidates = self.candidate_service.list_candidates()
            known_names = [c.get("name") for c in known_candidates if c.get("name")][:10]
            raise ValueError(
                f"Candidate '{candidate_query}' not found. Sample known candidates: {known_names}. You can also pass numeric user_id (e.g. 1)."
            )

        # Resolve candidate display name dynamically
        candidate_name = f"Candidate {user_id}"
        all_candidates = self.candidate_service.list_candidates()
        for c in all_candidates:
            if str(c.get("user_id")) == str(user_id) and c.get("name"):
                candidate_name = c["name"]
                break

        # Check if candidate vector chunks exist in ChromaDB
        existing_chunks = self.chroma_service.collection.get(
            where={"user_id": str(user_id)},
            include=["metadatas"],
        )
        vector_count = len(existing_chunks.get("ids", [])) if existing_chunks else 0

        # Auto-ingest if vector chunks not yet indexed in ChromaDB
        if vector_count == 0:
            logger.info("No vector chunks found in ChromaDB for user_id '%s'. Triggering auto S3 ingestion...", user_id)
            try:
                ingest_candidate_s3_transcripts(
                    user_id=user_id,
                    limit=3,
                    embedding_service=self.embedding_service,
                    chroma_service=self.chroma_service,
                )
            except Exception as exc:
                logger.warning("Auto S3 transcript ingestion for user_id '%s' skipped or completed with notice: %s", user_id, exc)

        # Retrieve relevant candidate-isolated interview turns
        sources = self.retriever.search_candidate(
            query=user_query,
            user_id=user_id,
            only_scored=only_scored,
            n_results=n_results,
        )

        # Construct grounded context for LLM synthesis
        context_blocks = []
        for idx, s in enumerate(sources, 1):
            strengths_str = ", ".join(s.get("strengths") or []) or "None highlighted"
            weaknesses_str = ", ".join(s.get("weaknesses") or []) or "None highlighted"
            missing_str = ", ".join(s.get("missing_concepts") or []) or "None highlighted"
            
            block = (
                f"--- TURN {idx} ---\n"
                f"Session ID: {s.get('session_id')}\n"
                f"Question: {s.get('question')}\n"
                f"Answer: {s.get('answer')}\n"
                f"Topic: {s.get('topic')} / Subtopic: {s.get('subtopic')}\n"
                f"Score: {s.get('score')}/10\n"
                f"Strengths: {strengths_str}\n"
                f"Weaknesses: {weaknesses_str}\n"
                f"Missing Concepts: {missing_str}\n"
                f"Feedback: {s.get('feedback', '')}\n"
            )
            context_blocks.append(block)

        context_str = "\n".join(context_blocks) if context_blocks else "No relevant interview Q&A turns found for this query."

        prompt = f"""You are an expert AI interview intelligence assistant analyzing technical interview performance for candidate '{candidate_name}' (User ID: {user_id}).

USER QUESTION:
"{user_query}"

RETRIEVED INTERVIEW EVIDENCE FOR {candidate_name}:
{context_str}

INSTRUCTIONS:
1. Synthesize a direct, clear, professional natural language response to the user's question based strictly on the retrieved interview evidence above.
2. Cite specific questions asked, candidate scores (e.g. 4/10), weaknesses, and missing concepts where applicable.
3. If the retrieved evidence does not contain relevant information to answer the question, state clearly that no specific interview evidence was found for this concept for candidate {candidate_name}.
4. Do not make up hypothetical scores or invent questions that were not asked.

Provide your response in clean markdown format:"""

        try:
            answer = self.llm_service.generate(prompt)
        except Exception as exc:
            logger.error("LLM generation failed: %s", exc)
            answer = f"Generated summary based on retrieved sources: Retained {len(sources)} Q&A evidence turn(s) for candidate {candidate_name}."

        # Save query log & answer to project MongoDB collection 'rag_candidate_reports'
        try:
            mongo_svc = MongoService()
            if mongo_svc.is_connected:
                report_doc = {
                    "report_type": "candidate_rag_qa",
                    "candidate_name": candidate_name,
                    "user_id": str(user_id),
                    "user_query": user_query,
                    "answer": answer,
                    "sources_retrieved_count": len(sources),
                    "timestamp": datetime.utcnow().isoformat(),
                }
                mongo_svc.save_candidate_report(report_doc)
        except Exception as exc:
            logger.warning("Saving candidate Q&A report to MongoDB skipped: %s", exc)

        return {
            "candidate_name": candidate_name,
            "user_id": str(user_id),
            "user_query": user_query,
            "answer": answer,
            "sources_retrieved_count": len(sources),
            "sources": sources,
        }
