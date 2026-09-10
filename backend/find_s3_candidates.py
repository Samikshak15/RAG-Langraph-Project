from app.services.candidate_service import CandidateService

def main():
    service = CandidateService()
    discovered = service.discover_candidates_from_s3()
    print(f"Total S3 candidates found: {len(discovered)}")
    for cand in discovered[:15]:
        print(f"user_id: {cand['user_id']} | name: {cand['name']} | object_count: {cand['s3_object_count']}")

if __name__ == "__main__":
    main()
