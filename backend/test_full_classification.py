from app.ingestion.transcript_parser import (
    parse_transcript,
    extract_qa_pairs,
)

from app.classification.topic_classifier import TopicClassifier


# Load transcript
with open(
    "data/sample_transcript.txt",
    "r",
    encoding="utf-8"
) as f:
    raw_text = f.read()


# Parse transcript
turns = parse_transcript(raw_text)

# Extract Q&A
qa_pairs = extract_qa_pairs(turns)

# Create classifier
classifier = TopicClassifier(
    "data/curriculum.json"
)


print("\n" + "=" * 100)
print(f"TOTAL Q&A: {len(qa_pairs)}")
print("=" * 100)


# Classify every Q&A
for qa in qa_pairs:

    result = classifier.classify(
        qa["question"],
        qa["answer"]
    )

    qa["topic"] = result["topic"]
    qa["subtopic"] = result["subtopic"]

    print("\n" + "-" * 100)
    print("Question ID:", qa["question_id"])
    print("Question:", qa["question"])
    print("Topic:", qa["topic"])
    print("Subtopic:", qa["subtopic"])