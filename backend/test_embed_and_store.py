from app.analysis.scoring import AnswerEvaluator
from app.classification.topic_classifier import TopicClassifier
from app.embeddings.embedding_service import EmbeddingService
from app.ingestion.chunk_builder import build_chunks
from app.ingestion.enrichment import build_enriched_records
from app.ingestion.metadata_extractor import (
    extract_s3_metadata,
    extract_session_start_time,
)
from app.ingestion.transcript_parser import extract_qa_pairs, parse_transcript
from app.vectorstore.chroma_service import ChromaService

s3_key = (
    "simulation_training/2071/358/"
    "995621c5-5724-4485-bab4-f6259d3ed391/"
    "995621c5-5724-4485-bab4-f6259d3ed391_transcript.txt"
)

with open("data/sample_transcript.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()

metadata = extract_s3_metadata(s3_key)

start_time = extract_session_start_time(raw_text)
metadata["session_start_time"] = start_time.isoformat() if start_time else None

turns = parse_transcript(raw_text)
qa_pairs = extract_qa_pairs(turns)

classifier = TopicClassifier("data/curriculum.json")
evaluator = AnswerEvaluator()

for qa in qa_pairs:
    classification = classifier.classify(qa["question"], qa["answer"])
    qa["topic"] = classification["topic"]
    qa["subtopic"] = classification["subtopic"]

    qa["evaluation"] = evaluator.evaluate(
        qa["question"],
        qa["answer"],
        topic=qa["topic"],
        subtopic=qa["subtopic"],
    )

records = build_enriched_records(qa_pairs, metadata)
chunks = build_chunks(records)

print(f"Total chunks: {len(chunks)}")

embedding_service = EmbeddingService()
chroma_service = ChromaService()

embeddings = embedding_service.embed_batch([c["text"] for c in chunks])
chroma_service.add_chunks(chunks, embeddings)

count = chroma_service.collection.count()
print(f"Collection count after upsert: {count}")
assert count == len(chunks), "Collection count does not match chunk count"

print("\n" + "=" * 100)
print("SEMANTIC QUERY: 'how do you evaluate RAG retrieval quality'")
print("=" * 100)

query_embedding = embedding_service.embed_text(
    "how do you evaluate RAG retrieval quality"
)
results = chroma_service.query(query_embedding, n_results=3)

for i, (chunk_id, distance) in enumerate(
    zip(results["ids"][0], results["distances"][0]), start=1
):
    print(f"{i}. {chunk_id}  (distance={distance:.4f})")

print("\n" + "=" * 100)
print("METADATA-FILTERED QUERY: where counts_toward_score = True")
print("=" * 100)

filtered_results = chroma_service.query(
    query_embedding, n_results=11, where={"counts_toward_score": True}
)
filtered_ids = filtered_results["ids"][0]
print("Matched chunk IDs:", filtered_ids)

not_covered_ids = {
    c["chunk_id"] for c in chunks if c["metadata"]["topic"] == "not_covered"
}
overlap = not_covered_ids & set(filtered_ids)
assert not overlap, f"not_covered chunks leaked into filtered results: {overlap}"

print("\n✅ Embedding + storage + retrieval verification passed!")
