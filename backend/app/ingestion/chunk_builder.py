import json
from datetime import datetime, timezone


def _serialize_list(values: list) -> str:
    """
    Chroma metadata only accepts scalar values, so list fields are
    serialized to a JSON string here. Reverse with json.loads(...) —
    e.g. for UI bullet rendering or a future reranking pass.
    """
    return json.dumps(values)


def build_chunk_id(session_id: str, question_id: str) -> str:
    return f"{session_id}_{question_id}"


def build_chunk_text(question: str, answer: str) -> str:
    return f"Question: {question}\nAnswer: {answer}"


def build_chunks(records: list[dict]) -> list[dict]:
    chunks = []

    for record in records:
        metadata = {
            "user_id": record["user_id"],
            "bot_id": record["bot_id"],
            "session_id": record["session_id"],
            "session_start_time": record["session_start_time"],

            "question_id": record["question_id"],
            "question": record["question"],
            "answer": record["answer"],

            "topic": record["topic"],
            "subtopic": record["subtopic"],

            "score": record["score"],
            "strengths": _serialize_list(record["strengths"]),
            "weaknesses": _serialize_list(record["weaknesses"]),
            "missing_concepts": _serialize_list(record["missing_concepts"]),
            "feedback": record["feedback"],
            "counts_toward_score": record["counts_toward_score"],

            "question_turn": record["question_turn"],
            "answer_turns": _serialize_list(record["answer_turns"]),

            "stored_at": datetime.now(timezone.utc).isoformat(),
        }

        chunks.append({
            "chunk_id": build_chunk_id(record["session_id"], record["question_id"]),
            "text": build_chunk_text(record["question"], record["answer"]),
            "metadata": metadata,
        })

    return chunks
