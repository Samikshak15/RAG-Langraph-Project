import urllib.request
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_live_qa():
    print("--- Testing Live Candidate RAG Q&A Engine Endpoint ---", flush=True)
    payload = {
        "candidate": "2071",
        "query": "What are the candidate's main technical achievements and weaknesses?",
        "n_results": 3,
        "only_scored": False,
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/candidate/query",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode("utf-8"))
        print("\n--- Live Endpoint Response Received ---", flush=True)
        print(f"Candidate Name: {res.get('candidate_name')}", flush=True)
        print(f"User ID: {res.get('user_id')}", flush=True)
        print(f"Query: {res.get('user_query')}", flush=True)
        print(f"Sources Retrieved Count: {res.get('sources_retrieved_count')}", flush=True)
        print(f"Answer:\n{res.get('answer')}\n", flush=True)
        if res.get("sources"):
            first_src = res["sources"][0]
            print(f"Sample Source Turn: Question: '{first_src.get('question')}' | Score: {first_src.get('score')}/10 | Rerank Score: {first_src.get('rerank_score')}", flush=True)
    except urllib.error.HTTPError as exc:
        print(f"HTTP Error {exc.code}: {exc.read().decode()}", flush=True)

if __name__ == "__main__":
    test_live_qa()
