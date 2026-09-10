# from app.ingestion.metadata_extractor import extract_s3_metadata


# s3_key = (
#     "simulation_training/"
#     "1086/"
#     "1/"
#     "06771bd0-3982-4ddc-b59e-f3398800a739/"
#     "06771bd0-3982-4ddc-b59e-f3398800a739_transcript.txt"
# )

# metadata = extract_s3_metadata(s3_key)

# print(metadata)

from app.ingestion.metadata_extractor import (
    extract_s3_metadata,
    extract_session_start_time,
)


s3_key = (
    "simulation_training/"
    "1086/"
    "1/"
    "06771bd0-3982-4ddc-b59e-f3398800a739/"
    "06771bd0-3982-4ddc-b59e-f3398800a739_transcript.txt"
)


with open(
    "data/sample_transcript.txt",
    "r",
    encoding="utf-8"
) as f:
    transcript = f.read()


# S3 metadata
metadata = extract_s3_metadata(s3_key)


# Session timestamp
start_time = extract_session_start_time(transcript)

metadata["session_start_time"] = (
    start_time.isoformat()
    if start_time
    else None
)


print(metadata)