from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


class PipelineRunRequest(BaseModel):
    source: Literal["local", "s3_latest"] = "local"


class QuestionResult(BaseModel):
    question_id: str
    question_turn: int
    answer_turns: list[int]
    question: str
    answer: str
    topic: str
    subtopic: str
    score: int
    strengths: list[str]
    weaknesses: list[str]
    missing_concepts: list[str]
    feedback: str
    counts_toward_score: bool


class PipelineSummary(BaseModel):
    total_questions: int
    scored_questions: int
    not_covered_questions: int
    average_score: float
    topics_covered: list[str]


class PipelineRunResponse(BaseModel):
    session_id: str
    user_id: str
    bot_id: str
    source_key: str
    session_start_time: Optional[datetime]
    results: list[QuestionResult]
    summary: PipelineSummary
    chunks_stored: int
    collection_count: int


class SearchRequest(BaseModel):
    query: str = Field(min_length=1)
    only_scored: bool = False
    n_results: int = Field(default=5, ge=1, le=20)


class SearchResult(BaseModel):
    chunk_id: str
    text: str
    distance: float
    rerank_score: float
    session_id: str
    user_id: str
    question_id: str
    question: str
    answer: str
    topic: str
    subtopic: str
    score: int
    strengths: list[str]
    weaknesses: list[str]
    missing_concepts: list[str]
    feedback: str
    counts_toward_score: bool


class SearchResponse(BaseModel):
    query: str
    results: list[SearchResult]


class HealthResponse(BaseModel):
    status: Literal["ok"]
    chroma_collection_count: int


class ChunkListItem(BaseModel):
    chunk_id: str
    question_id: str
    session_id: str
    topic: str
    subtopic: str
    score: int
    counts_toward_score: bool
    stored_at: Optional[str]


class ChunkListResponse(BaseModel):
    chunks: list[ChunkListItem]
    total: int
    limit: int
    offset: int


class StatsResponse(BaseModel):
    total_chunks: int
    distinct_sessions: int
    avg_score: float
    vector_store_bytes: int
    last_stored_at: Optional[str]
