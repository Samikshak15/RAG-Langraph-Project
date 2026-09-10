from unittest.mock import MagicMock, patch
from app.services.candidate_service import CandidateService


def test_numeric_user_id_direct():
    service = CandidateService()
    # Numeric user_ids work directly without any hardcoding
    assert service.resolve_user_id("1756") == "1756"
    assert service.resolve_user_id("2071") == "2071"
    assert service.resolve_user_id("9999") == "9999"
    print("[OK] test_numeric_user_id_direct PASSED")


def test_mongodb_user_resolution():
    mock_mongo = MagicMock()
    mock_mongo.is_connected = True
    mock_mongo.find_user_id_by_name.side_effect = lambda name: "1756" if "nayan" in name.lower() else None
    mock_mongo.list_all_users_from_mongo.return_value = [
        {"user_id": "1756", "name": "Nayan Kumar", "email": "nayan@example.com", "source": "mongo_db"}
    ]

    with patch("app.services.mongo_service.MongoService", return_value=mock_mongo):
        service = CandidateService()
        resolved_id = service.resolve_user_id("Nayan")
        assert resolved_id == "1756"

        candidates = service.list_candidates()
        assert len(candidates) == 1
        assert candidates[0]["user_id"] == "1756"
        assert candidates[0]["name"] == "Nayan Kumar"
        print("[OK] test_mongodb_user_resolution PASSED")


if __name__ == "__main__":
    test_numeric_user_id_direct()
    test_mongodb_user_resolution()
    print("All MongoDB candidate resolution tests passed successfully!")
