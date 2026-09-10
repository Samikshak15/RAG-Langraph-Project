from app.services.s3_service import S3Service
from app.ingestion.transcript_parser import parse_transcript, extract_qa_pairs

def inspect():
    s3 = S3Service()
    keys = [
        "simulation_training/2071/358/995621c5-5724-4485-bab4-f6259d3ed391/995621c5-5724-4485-bab4-f6259d3ed391_transcript.txt",
        "simulation_training/1086/1/06771bd0-3982-4ddc-b59e-f3398800a739/06771bd0-3982-4ddc-b59e-f3398800a739_transcript.txt",
        "simulation_training/1/37/f3d78001-48b7-4bd9-8be9-6f723cb75ea2/f3d78001-48b7-4bd9-8be9-6f723cb75ea2_transcript.txt",
    ]
    for key in keys:
        try:
            raw_text = s3.get_object(key).decode("utf-8", errors="ignore")
            turns = parse_transcript(raw_text)
            qa = extract_qa_pairs(turns)
            print(f"Key: {key}\n  Raw len: {len(raw_text)} | Turns: {len(turns)} | Q&A pairs: {len(qa)}")
            print(f"  First 150 chars: {repr(raw_text[:150])}\n")
        except Exception as exc:
            print(f"Key: {key} ERROR: {exc}\n")

if __name__ == "__main__":
    inspect()
