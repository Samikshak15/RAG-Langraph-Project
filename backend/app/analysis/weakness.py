from collections import Counter
from typing import Any


def aggregate_weakness_patterns(session_records_list: list[list[dict]]) -> dict[str, Any]:
    """
    Aggregates weakness patterns, missing concepts, and recurring low scores
    across multiple interview sessions for a single candidate.
    """
    total_questions = 0
    all_weaknesses: list[str] = []
    all_missing_concepts: list[str] = []
    topic_scores: dict[str, list[int]] = {}
    repeated_wrong_answers: list[dict] = []
    topic_error_counts: Counter = Counter()

    for session_idx, records in enumerate(session_records_list):
        for rec in records:
            total_questions += 1
            score = rec.get("score", 0)
            topic = rec.get("topic", "general")
            subtopic = rec.get("subtopic", "general")
            question = rec.get("question", "")

            # Track scores per topic
            topic_scores.setdefault(topic, []).append(score)

            # Track low-scoring questions (< 5/10)
            if score < 5 and rec.get("counts_toward_score", True):
                topic_error_counts[topic] += 1
                topic_error_counts[f"{topic} :: {subtopic}"] += 1
                repeated_wrong_answers.append({
                    "session_index": session_idx + 1,
                    "session_id": rec.get("session_id"),
                    "question": question,
                    "topic": topic,
                    "subtopic": subtopic,
                    "score": score,
                    "weaknesses": rec.get("weaknesses", []),
                    "missing_concepts": rec.get("missing_concepts", []),
                })

            # Collect qualitative feedback lists
            all_weaknesses.extend(rec.get("weaknesses", []))
            all_missing_concepts.extend(rec.get("missing_concepts", []))

    # Frequency counting for recurring gaps
    missing_concepts_freq = Counter(all_missing_concepts).most_common(10)
    recurring_technical_gaps = [
        {"concept": concept, "occurrence_count": count}
        for concept, count in missing_concepts_freq if count >= 1
    ]

    # Rank priority topics to work on
    topics_to_improve = []
    for topic_name, count in topic_error_counts.most_common(10):
        scores = topic_scores.get(topic_name.split(" :: ")[0], [5])
        avg_score = round(sum(scores) / len(scores), 2) if scores else 0.0
        topics_to_improve.append({
            "topic": topic_name,
            "error_count": count,
            "avg_score": avg_score,
            "recommendation": f"Review technical fundamentals for {topic_name}. Practice targeted Q&A."
        })

    return {
        "total_questions_evaluated": total_questions,
        "repeated_wrong_answers": repeated_wrong_answers,
        "recurring_technical_gaps": recurring_technical_gaps,
        "topics_to_improve": topics_to_improve,
        "top_weaknesses": Counter(all_weaknesses).most_common(5),
    }
