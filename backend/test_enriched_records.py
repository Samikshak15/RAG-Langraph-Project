import json

from app.analysis.scoring import AnswerEvaluator
from app.classification.topic_classifier import TopicClassifier
from app.ingestion.enrichment import build_enriched_records
from app.ingestion.metadata_extractor import (
    extract_s3_metadata,
    extract_session_start_time,
)
from app.ingestion.transcript_parser import extract_qa_pairs, parse_transcript

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

print(f"Total enriched records: {len(records)}\n")

for record in records:
    print("=" * 100)
    print(json.dumps(record, indent=2))
