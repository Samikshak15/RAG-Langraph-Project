from app.services.mongo_service import MongoService

def fetch_and_print_candidates():
    mongo = MongoService()
    if not mongo.is_connected:
        print("Could not connect to MongoDB")
        return
    
    users = mongo.list_all_users_from_mongo()
    print(f"TOTAL CANDIDATES: {len(users)}")
    for u in users:
        print(f"ID: {u['user_id']} | Name: {u['name']} | Email: {u.get('email', '')}")

if __name__ == "__main__":
    fetch_and_print_candidates()
