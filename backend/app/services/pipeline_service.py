import logging
from app.analysis.scoring import AnswerEvaluator

logger = logging.getLogger(__name__)
from app.classification.topic_classifier import TopicClassifier
from app.config import CURRICULUM_PATH, SAMPLE_TRANSCRIPT_PATH
from app.embeddings.embedding_service import EmbeddingService
from app.ingestion.chunk_builder import build_chunks
from app.ingestion.enrichment import build_enriched_records
from app.ingestion.metadata_extractor import (
    extract_s3_metadata,
    extract_session_start_time,
)
from app.ingestion.transcript_parser import extract_qa_pairs, parse_transcript
from app.services.candidate_service import CandidateService
from app.services.s3_service import S3Service
from app.vectorstore.chroma_service import ChromaService

# Same fixture key already verified in test_embed_and_store.py / test_enriched_records.py —
# the local sample transcript has no real S3 key of its own, so we reuse it.
LOCAL_SAMPLE_S3_KEY = (
    "simulation_training/2071/358/"
    "995621c5-5724-4485-bab4-f6259d3ed391/"
    "995621c5-5724-4485-bab4-f6259d3ed391_transcript.txt"
)


def _load_transcript(source: str) -> tuple[str, str]:
    if source == "local":
        with open(SAMPLE_TRANSCRIPT_PATH, "r", encoding="utf-8") as f:
            return f.read(), LOCAL_SAMPLE_S3_KEY

    if source == "s3_latest":
        s3 = S3Service()
        objects = s3.list_objects(prefix="simulation_training/")
        transcripts = [o for o in objects if o["Key"].endswith("_transcript.txt")]
        if not transcripts:
            raise ValueError("No transcript objects found in S3 under 'simulation_training/'")
        latest = max(transcripts, key=lambda o: o["LastModified"])
        return s3.get_object(latest["Key"]).decode("utf-8"), latest["Key"]

    raise ValueError(f"Unknown source: {source}")


def run_pipeline_for_transcript(
    raw_text: str,
    s3_key: str,
    embedding_service: EmbeddingService,
    chroma_service: ChromaService,
) -> dict:
    metadata = extract_s3_metadata(s3_key)
    start_time = extract_session_start_time(raw_text)
    metadata["session_start_time"] = start_time.isoformat() if start_time else None

    turns = parse_transcript(raw_text)
    qa_pairs = extract_qa_pairs(turns)
    if not qa_pairs:
        raise ValueError("No question/answer pairs could be extracted from this transcript")

    classifier = TopicClassifier(CURRICULUM_PATH)
    evaluator = AnswerEvaluator()

    for qa in qa_pairs:
        classification = classifier.classify(qa["question"], qa["answer"])
        qa["topic"] = classification["topic"]
        qa["subtopic"] = classification["subtopic"]
        qa["evaluation"] = evaluator.evaluate(
            qa["question"], qa["answer"], topic=qa["topic"], subtopic=qa["subtopic"],
        )

    records = build_enriched_records(qa_pairs, metadata)
    chunks = build_chunks(records)

    if chunks:
        embeddings = embedding_service.embed_batch([c["text"] for c in chunks])
        chroma_service.add_chunks(chunks, embeddings)
    collection_count = chroma_service.collection.count()

    scored = [r for r in records if r["counts_toward_score"]]
    summary = {
        "total_questions": len(records),
        "scored_questions": len(scored),
        "not_covered_questions": len(records) - len(scored),
        "average_score": round(sum(r["score"] for r in scored) / len(scored), 2) if scored else 0.0,
        "topics_covered": sorted({r["topic"] for r in scored}),
    }

    return {
        "session_id": metadata["session_id"],
        "user_id": metadata["user_id"],
        "bot_id": metadata["bot_id"],
        "source_key": metadata["source_key"],
        "session_start_time": metadata["session_start_time"],
        "results": records,
        "summary": summary,
        "chunks_stored": len(chunks),
        "collection_count": collection_count,
    }


def run_pipeline(source: str, embedding_service: EmbeddingService, chroma_service: ChromaService) -> dict:
    raw_text, s3_key = _load_transcript(source)
    return run_pipeline_for_transcript(raw_text, s3_key, embedding_service, chroma_service)


def ingest_candidate_s3_transcripts(
    user_id: str,
    limit: int,
    embedding_service: EmbeddingService,
    chroma_service: ChromaService,
) -> dict:
    candidate_service = CandidateService()
    sessions = candidate_service.get_candidate_sessions(user_id, limit=limit)

    if not sessions:
        raise ValueError(f"No completed interview sessions found in S3 for user_id '{user_id}'")

    s3_service = S3Service()

    total_chunks = 0
    total_qa = 0
    processed_sessions = 0

    for s_meta in sessions:
        s3_key = s_meta.get("source_key")
        if not s3_key:
            continue
        try:
            raw_text = s_meta.get("raw_text")
            if not raw_text:
                raw_bytes = s3_service.get_object(s3_key)
                raw_text = raw_bytes.decode("utf-8", errors="ignore")

            res = run_pipeline_for_transcript(raw_text, s3_key, embedding_service, chroma_service)
            total_qa += len(res.get("results", []))
            total_chunks += res.get("chunks_stored", 0)
            processed_sessions += 1
        except Exception as exc:
            logger.warning("Error ingesting session S3 key '%s': %s", s3_key, exc, exc_info=True)

    return {
        "status": "success",
        "user_id": user_id,
        "sessions_found": len(sessions),
        "sessions_processed": processed_sessions,
        "total_qa_evaluated": total_qa,
        "chunks_stored": total_chunks,
        "collection_count_after_ingestion": chroma_service.collection.count(),
    }


