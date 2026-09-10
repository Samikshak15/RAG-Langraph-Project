from pathlib import PurePosixPath


def extract_s3_metadata(s3_key: str) -> dict:
    """
    Extract interview metadata from the S3 object key.

    Expected format:

    simulation_training/{user_id}/{bot_id}/{session_id}/filename
    """

    path = PurePosixPath(s3_key)

    parts = path.parts

    if len(parts) < 5:
        raise ValueError(
            f"Unexpected S3 key format: {s3_key}"
        )

    if parts[0] != "simulation_training":
        raise ValueError(
            f"Unexpected S3 prefix: {parts[0]}"
        )

    user_id = parts[1]
    bot_id = parts[2]
    session_id = parts[3]
    filename = parts[4]

    return {
        "user_id": user_id,
        "bot_id": bot_id,
        "session_id": session_id,
        "filename": filename,
        "source_key": s3_key,
    }


import re
from datetime import datetime


TIMESTAMP_PATTERN = re.compile(
    r"\[(?P<timestamp>\d{4}-\d{2}-\d{2}T[^\]]+)\]"
)


def extract_session_start_time(text: str):
    """
    Extract the timestamp of the first transcript turn.
    """

    match = TIMESTAMP_PATTERN.search(text)

    if not match:
        return None

    timestamp = match.group("timestamp")

    return datetime.fromisoformat(timestamp)