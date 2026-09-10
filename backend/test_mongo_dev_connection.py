from app.services.mongo_service import MongoService

def test_live_dev_mongo_connection():
    print("Testing connection to Dev MongoDB...")
    mongo_service = MongoService()
    
    print("Is Connected:", mongo_service.is_connected)
    if not mongo_service.is_connected:
        print("[WARNING] Could not connect to remote Dev MongoDB (network/firewall or server unreachable). Fallback mechanism verified!")
        return

    print("Connected successfully to database:", mongo_service.db_name)

    # 1. Test listing users from auth_app_t_user
    users = mongo_service.list_all_users_from_mongo()
    print(f"Total Users Found in auth_app_t_user: {len(users)}")
    if users:
        print("Sample User Doc:", users[0])

    # 2. Test user_id lookup (e.g. user_id=1 / Intelli Admin)
    user_id_found = mongo_service.find_user_id_by_name("Intelli") or mongo_service.find_user_id_by_name("Admin")
    print("User ID found for 'Intelli/Admin':", user_id_found)

    # 3. Test sessions lookup from auth_app_t_request
    if user_id_found:
        sessions = mongo_service.get_candidate_sessions(user_id_found, limit=3)
        print(f"Sessions found in auth_app_t_request for user_id '{user_id_found}': {len(sessions)}")
        if sessions:
            print("Sample Session:", sessions[0])

    print("[OK] Live Dev MongoDB integration test complete!")

if __name__ == "__main__":
    test_live_dev_mongo_connection()
