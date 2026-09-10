import urllib.request
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_api_flow():
    print("--- 1. Testing GET /api/v1/candidates (used by CandidateSelector) ---", flush=True)
    req = urllib.request.Request(f"{BASE_URL}/candidates?limit=10")
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    print(f"Total Candidates: {data.get('total_candidates')}, Returned: {len(data.get('candidates', []))}", flush=True)
    if data.get("candidates"):
        print(f"Sample Candidate: {data['candidates'][0]}", flush=True)

    print("\n--- 2. Testing POST /api/v1/candidate/query (used by CandidateRAGPanel) ---", flush=True)
    payload = json.dumps({"candidate": "2071", "query": "What are candidate strengths?"}).encode("utf-8")
    req = urllib.request.Request(f"{BASE_URL}/candidate/query", data=payload, headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode("utf-8"))
    print(f"Candidate: {res.get('candidate_name')} | User ID: {res.get('user_id')} | Sources: {res.get('sources_retrieved_count')}", flush=True)

if __name__ == "__main__":
    test_api_flow()
