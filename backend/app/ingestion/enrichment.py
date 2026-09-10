def build_enriched_records(qa_pairs: list[dict], metadata: dict) -> list[dict]:
    records = []

    for qa in qa_pairs:
        evaluation = qa["evaluation"]

        records.append({
            "user_id": metadata["user_id"],
            "bot_id": metadata["bot_id"],
            "session_id": metadata["session_id"],
            "session_start_time": metadata["session_start_time"],

            "question_id": qa["question_id"],
            "question_turn": qa["question_turn"],
            "answer_turns": qa["answer_turns"],

            "question": qa["question"],
            "answer": qa["answer"],

            "topic": qa["topic"],
            "subtopic": qa["subtopic"],

            "score": evaluation["score"],
            "strengths": evaluation["strengths"],
            "weaknesses": evaluation["weaknesses"],
            "missing_concepts": evaluation["missing_concepts"],
            "feedback": evaluation["feedback"],

            "counts_toward_score": evaluation["counts_toward_score"],
        })

    return records
