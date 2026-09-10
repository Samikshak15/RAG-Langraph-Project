import urllib.request
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_live_ingest():
    print("--- 1. Checking Stats Before Ingestion ---", flush=True)
    req = urllib.request.Request(f"{BASE_URL}/stats")
    with urllib.request.urlopen(req) as resp:
        stats_before = json.loads(resp.read().decode())
    print(f"Stats Before: {stats_before}", flush=True)

    print("\n--- 2. Triggering Candidate Ingestion Endpoint ---", flush=True)
    ingest_url = f"{BASE_URL}/candidate/2071/ingest?limit=1"
    req = urllib.request.Request(ingest_url, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            ingest_res = json.loads(resp.read().decode())
        print(f"Ingestion Result: {ingest_res}", flush=True)
    except urllib.error.HTTPError as exc:
        err_body = exc.read().decode()
        print(f"HTTPError {exc.code}: {err_body}", flush=True)
        return

    print("\n--- 3. Checking Stats After Ingestion ---", flush=True)
    req = urllib.request.Request(f"{BASE_URL}/stats")
    with urllib.request.urlopen(req) as resp:
        stats_after = json.loads(resp.read().decode())
    print(f"Stats After: {stats_after}", flush=True)

    print("\n--- 4. Inspecting Chunks in Vector Store ---", flush=True)
    req = urllib.request.Request(f"{BASE_URL}/chunks?limit=5")
    with urllib.request.urlopen(req) as resp:
        chunks_res = json.loads(resp.read().decode())
    print(f"Total Chunks: {chunks_res.get('total_chunks')}, Returned: {len(chunks_res.get('chunks', []))}", flush=True)
    if chunks_res.get('chunks'):
        print(f"Sample Chunk Metadata: {chunks_res['chunks'][0].get('metadata')}", flush=True)


if __name__ == "__main__":
    test_live_ingest()
