from fastapi import APIRouter, HTTPException, Request

from app.models.candidate_schemas import (
    CandidateAnalysisRequest,
    CandidateAnalysisResponse,
    CandidateHistoryResponse,
    CandidateQueryRequest,
    CandidateQueryResponse,
)
from app.models.schemas import (
    ChunkListResponse,
    HealthResponse,
    PipelineRunRequest,
    PipelineRunResponse,
    SearchRequest,
    SearchResponse,
    StatsResponse,
)
from app.services.pipeline_service import (
    ingest_candidate_s3_transcripts,
    run_pipeline,
    run_pipeline_for_transcript,
)
from app.services.vector_store_service import compute_stats, list_chunks

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health(request: Request):
    chroma_service = request.app.state.chroma_service
    return {"status": "ok", "chroma_collection_count": chroma_service.collection.count()}


@router.post("/pipeline/run", response_model=PipelineRunResponse)
def pipeline_run(body: PipelineRunRequest, request: Request):
    embedding_service = request.app.state.embedding_service
    chroma_service = request.app.state.chroma_service
    try:
        return run_pipeline(body.source, embedding_service, chroma_service)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Pipeline run failed: {exc}") from exc


@router.post("/search", response_model=SearchResponse)
def search(body: SearchRequest, request: Request):
    retriever = request.app.state.retriever
    try:
        results = retriever.search(body.query, body.only_scored, body.n_results)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Search failed: {exc}") from exc
    return {"query": body.query, "results": results}


@router.get("/stats", response_model=StatsResponse)
def stats(request: Request):
    chroma_service = request.app.state.chroma_service
    return compute_stats(chroma_service)


@router.get("/chunks", response_model=ChunkListResponse)
def chunks(request: Request, limit: int = 20, offset: int = 0):
    chroma_service = request.app.state.chroma_service
    return list_chunks(chroma_service, limit, offset)


@router.get("/candidate/{query}/history", response_model=CandidateHistoryResponse)
def candidate_history(query: str, limit: int = 3):
    from app.services.candidate_service import CandidateService
    candidate_service = CandidateService()
    user_id = candidate_service.resolve_user_id(query)
    if not user_id:
        known_candidates = candidate_service.list_candidates()
        known_names = [c.get("name") for c in known_candidates if c.get("name")][:10]
        raise HTTPException(
            status_code=404,
            detail=f"Candidate '{query}' not found. Sample MongoDB candidates: {known_names}. You can also pass numeric user_id (e.g. 1)."
        )
    
    sessions = candidate_service.get_candidate_sessions(user_id, limit=limit)
    return {
        "candidate_query": query,
        "resolved_user_id": user_id,
        "total_sessions_found": len(sessions),
        "sessions": sessions,
    }


@router.post("/candidate/{query}/ingest")
def ingest_candidate_transcripts(query: str, request: Request, limit: int = 3):
    from app.services.candidate_service import CandidateService
    candidate_service = CandidateService()
    user_id = candidate_service.resolve_user_id(query)
    if not user_id:
        known_candidates = candidate_service.list_candidates()
        known_names = [c.get("name") for c in known_candidates if c.get("name")][:10]
        raise HTTPException(
            status_code=404,
            detail=f"Candidate '{query}' not found. Sample MongoDB candidates: {known_names}. You can also pass numeric user_id (e.g. 1)."
        )

    embedding_service = request.app.state.embedding_service
    chroma_service = request.app.state.chroma_service

    try:
        res = ingest_candidate_s3_transcripts(
            user_id=user_id,
            limit=limit,
            embedding_service=embedding_service,
            chroma_service=chroma_service,
        )
        res["candidate_query"] = query
        return res
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {exc}") from exc



@router.post("/candidate/register")
def register_candidate(user_id: str, name: str, email: str = None):
    from app.services.candidate_service import CandidateService
    candidate_service = CandidateService()
    entry = candidate_service.register_candidate(user_id=user_id, name=name, email=email)
    return {"message": "Candidate registered successfully", "candidate": entry}


@router.get("/candidates")
def list_candidates(auto_discover: bool = False, limit: int = 2000, search: str = None):
    from app.services.candidate_service import CandidateService
    candidate_service = CandidateService()
    candidates = candidate_service.list_candidates(auto_discover=auto_discover, limit=limit, search=search)
    return {
        "auto_discover": auto_discover,
        "total_candidates": len(candidates),
        "candidates": candidates,
    }


@router.post("/candidate/analyze", response_model=CandidateAnalysisResponse)
def analyze_candidate(body: CandidateAnalysisRequest, request: Request):
    from app.analysis.comparison import MultiInterviewAnalyzer
    from app.analysis.report_generator import ReportGenerator
    from app.services.candidate_service import CandidateService

    candidate_service = CandidateService()
    user_id = candidate_service.resolve_user_id(body.candidate)
    if not user_id:
        known_candidates = candidate_service.list_candidates()
        known_names = [c.get("name") for c in known_candidates if c.get("name")][:10]
        raise HTTPException(
            status_code=404,
            detail=f"Candidate '{body.candidate}' not found. Sample MongoDB candidates: {known_names}. You can also pass numeric user_id (e.g. 1)."
        )

    # 1. Discover sessions for candidate
    sessions_meta = candidate_service.get_candidate_sessions(user_id, limit=body.num_interviews)

    embedding_service = request.app.state.embedding_service
    chroma_service = request.app.state.chroma_service

    evaluated_sessions = []
    if sessions_meta:
        from app.services.s3_service import S3Service
        s3_svc = S3Service()
        for meta in sessions_meta:
            try:
                s3_key = meta.get("source_key")
                raw_text = meta.get("raw_text")
                if not raw_text and s3_key:
                    raw_bytes = s3_svc.get_object(s3_key)
                    raw_text = raw_bytes.decode("utf-8", errors="ignore")

                if raw_text and s3_key:
                    s_data = run_pipeline_for_transcript(raw_text, s3_key, embedding_service, chroma_service)
                    evaluated_sessions.append(s_data)
            except Exception:
                pass

    if not evaluated_sessions:
        # Fallback to local sample transcript if S3 credentials not set
        s_data = run_pipeline("local", embedding_service, chroma_service)
        s_data["session_id"] = f"session_{user_id}_sample"
        evaluated_sessions.append(s_data)

    analyzer = MultiInterviewAnalyzer()
    analysis_result = analyzer.analyze_candidate_history(
        candidate_name=body.candidate, user_id=user_id, sessions_data=evaluated_sessions
    )

    reporter = ReportGenerator()
    report = reporter.generate_report(analysis_result, user_query=body.query)

    # Save generated report to project collection rag_candidate_reports
    try:
        from app.services.mongo_service import MongoService
        mongo_service = MongoService()
        if mongo_service.is_connected:
            mongo_service.save_candidate_report(report)
    except Exception as exc:
        pass

    return report


@router.post("/candidate/query", response_model=CandidateQueryResponse)
def query_candidate(body: CandidateQueryRequest, request: Request):
    from app.services.rag_qa_service import CandidateQAService

    embedding_service = request.app.state.embedding_service
    chroma_service = request.app.state.chroma_service
    reranker_service = request.app.state.reranker_service

    qa_service = CandidateQAService(
        embedding_service=embedding_service,
        chroma_service=chroma_service,
        reranker_service=reranker_service,
    )

    try:
        return qa_service.answer_candidate_query(
            candidate_query=body.candidate,
            user_query=body.query,
            n_results=body.n_results,
            only_scored=body.only_scored,
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Candidate Q&A query failed: {exc}") from exc





