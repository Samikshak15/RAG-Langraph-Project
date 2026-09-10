from app.analysis.scoring import AnswerEvaluator
from app.classification.topic_classifier import TopicClassifier
from app.ingestion.transcript_parser import extract_qa_pairs, parse_transcript

with open("data/sample_transcript.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()

turns = parse_transcript(raw_text)
qa_pairs = extract_qa_pairs(turns)

classifier = TopicClassifier("data/curriculum.json")
evaluator = AnswerEvaluator()

print(f"Total Q&A pairs: {len(qa_pairs)}\n")

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

    print("=" * 100)
    print(qa["question_id"], "->", qa["topic"], "/", qa["subtopic"])
    print("Q:", qa["question"][:200])
    print("A:", qa["answer"][:200])

    ev = qa["evaluation"]
    tag = "" if ev["counts_toward_score"] else "  [off-curriculum, not scored toward coverage]"
    print(f"Score: {ev['score']}/10{tag}")
    print("Strengths:", ev["strengths"])
    print("Weaknesses:", ev["weaknesses"])
    print("Missing concepts:", ev["missing_concepts"])
    print("Feedback:", ev["feedback"])
