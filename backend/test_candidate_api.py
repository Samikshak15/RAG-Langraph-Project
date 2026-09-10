from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_candidate_history_api():
    # Test valid candidate lookup (Samiksha)
    response = client.get("/api/v1/candidate/Samiksha/history?limit=3")
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())
    assert response.status_code == 200
    data = response.json()
    assert data["candidate_query"] == "Samiksha"
    assert data["resolved_user_id"] == "2071"
    assert "sessions" in data
    print("[OK] test_candidate_history_api PASSED")

def test_candidate_not_found_api():
    response = client.get("/api/v1/candidate/UnknownPerson/history")
    assert response.status_code == 404
    print("[OK] test_candidate_not_found_api PASSED")

if __name__ == "__main__":
    test_candidate_history_api()
    test_candidate_not_found_api()
    print("All Candidate API integration tests passed successfully!")
