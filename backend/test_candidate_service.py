from unittest.mock import MagicMock, patch
from app.services.candidate_service import CandidateService


def test_resolve_user_id_direct_numeric():
    service = CandidateService()
    # Numeric IDs work directly without any hardcoding
    assert service.resolve_user_id("2071") == "2071"
    assert service.resolve_user_id("1756") == "1756"
    print("[OK] test_resolve_user_id_direct_numeric PASSED")


def test_resolve_user_id_from_mongodb():
    mock_mongo = MagicMock()
    mock_mongo.is_connected = True
    mock_mongo.find_user_id_by_name.side_effect = lambda name: "2071" if "samiksha" in name.lower() else ("1756" if "nayan" in name.lower() else None)

    with patch("app.services.mongo_service.MongoService", return_value=mock_mongo):
        service = CandidateService()
        assert service.resolve_user_id("Samiksha") == "2071"
        assert service.resolve_user_id("samiksha") == "2071"
        assert service.resolve_user_id("Nayan") == "1756"
        assert service.resolve_user_id("NonExistentCandidate") is None
        print("[OK] test_resolve_user_id_from_mongodb PASSED")


def test_get_candidate_sessions_mock():
    mock_s3 = MagicMock()
    mock_s3.list_objects.return_value = [
        {
            "Key": "simulation_training/2071/358/session1/session1_transcript.txt",
            "Size": 1024,
            "LastModified": "2026-01-01T10:00:00Z"
        }
    ]
    mock_s3.get_object.return_value = b"[2026-01-01T10:00:00Z] Interviewer: Hello"

    service = CandidateService(s3_service=mock_s3)
    sessions = service.get_candidate_sessions(user_id="2071", limit=1)
    assert len(sessions) == 1
    assert sessions[0]["user_id"] == "2071"
    print("[OK] test_get_candidate_sessions_mock PASSED")


if __name__ == "__main__":
    test_resolve_user_id_direct_numeric()
    test_resolve_user_id_from_mongodb()
    test_get_candidate_sessions_mock()
    print("All CandidateService unit tests passed successfully!")
