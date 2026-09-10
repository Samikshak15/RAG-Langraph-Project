from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, Field


class CandidateProfile(BaseModel):
    user_id: str
    name: str
    email: Optional[str] = None
    total_sessions: int = 0


class CandidateSessionMeta(BaseModel):
    session_id: str
    user_id: str
    bot_id: str
    source_key: str
    session_start_time: Optional[datetime] = None
    file_size_bytes: int = 0


class CandidateHistoryResponse(BaseModel):
    candidate_query: str
    resolved_user_id: str
    total_sessions_found: int
    sessions: list[CandidateSessionMeta]


class CandidateAnalysisRequest(BaseModel):
    query: str = Field(
        default="What are the candidate's main weaknesses across recent interviews?",
        description="Natural language query about candidate performance",
    )
    candidate: str = Field(
        ...,
        description="Candidate name (e.g. 'Samiksha', 'Nayan') or user_id (e.g. '2071')",
    )
    num_interviews: int = Field(default=3, ge=1, le=10, description="Number of recent interviews to compare")


class CandidateAnalysisResponse(BaseModel):
    candidate_name: str
    user_id: str
    user_query: str
    sessions_analyzed: int
    overall_score: float
    performance_trend: str
    executive_summary: str
    session_summaries: list[dict[str, Any]]
    repeated_wrong_answers: list[dict[str, Any]]
    recurring_technical_gaps: list[dict[str, Any]]
    topics_to_work_on: list[dict[str, Any]]


class CandidateQueryRequest(BaseModel):
    candidate: str = Field(
        ...,
        description="Candidate name or numeric user_id",
    )
    query: str = Field(
        ...,
        description="Natural language question about the candidate's interview performance or concepts",
    )
    n_results: int = Field(default=5, ge=1, le=20, description="Number of relevant interview Q&A turns to retrieve")
    only_scored: bool = Field(default=False, description="Filter only Q&A turns that count toward score")


class CandidateQueryResponse(BaseModel):
    candidate_name: str
    user_id: str
    user_query: str
    answer: str
    sources_retrieved_count: int
    sources: list[dict[str, Any]]

