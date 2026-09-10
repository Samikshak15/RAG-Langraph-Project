from app.classification.topic_classifier import TopicClassifier
from app.ingestion.transcript_parser import extract_qa_pairs, parse_transcript

with open("data/sample_transcript.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()

turns = parse_transcript(raw_text)
qa_pairs = extract_qa_pairs(turns)

classifier = TopicClassifier("data/curriculum.json")

print(f"Total Q&A pairs: {len(qa_pairs)}\n")

for qa in qa_pairs:
    result = classifier.classify(qa["question"], qa["answer"])

    qa["topic"] = result["topic"]
    qa["subtopic"] = result["subtopic"]

    print("=" * 100)
    print(qa["question_id"], "->", result["topic"], "/", result["subtopic"])
    print("Q:", qa["question"][:200])
    print("A:", qa["answer"][:200])
