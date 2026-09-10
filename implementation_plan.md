# Implementation Plan: Interview Intelligence RAG & LangGraph Multi-Interview Pattern Analysis

This implementation plan evaluates the current state of your repository against your target use case, details what is currently implemented vs. what is missing, and provides a step-by-step technical plan to complete the application **without modifying any existing code today** (as requested).

---

## Current State Analysis (Implemented vs. Missing)

### 1. Store & Retrieve Metadata and Transcripts
- **Implemented**:
  - S3 key parsing (`extract_s3_metadata`) extracting `user_id`, `bot_id`, `session_id`, `source_key` (`app/ingestion/metadata_extractor.py`).
  - Interview date/timestamp parsing (`extract_session_start_time`).
  - ChromaDB vector store for chunked Q&A pairs with metadata enrichment (`app/vectorstore/chroma_service.py`).
  - Hybrid vector search with Cohere re-ranking (`app/rag/retriever.py`).
- **Missing / Needs Extension**:
  - **Candidate Name Mapping**: Current metadata stores `user_id` (e.g., `"2071"`). Querying by name (e.g., *"Samiksha"*) requires mapping `candidate_name` $\leftrightarrow$ `user_id` or storing `candidate_name` in metadata.
  - **Candidate-Filtered Retrieval**: Chroma queries need filtering by `user_id`/`candidate_name` across multiple session IDs.

### 2. LangGraph Pipeline Architecture
- **Implemented**:
  - `langgraph>=0.0.30` dependency added in `requirements.txt`.
- **Missing**:
  - **No LangGraph graph code exists yet**. Current pipeline (`app/services/pipeline_service.py`) is a standard procedural script for single-transcript ingestion.
  - Needed: LangGraph StateGraph nodes for Query Understanding, Latest Sessions Retrieval, S3 Transcript Fetching, Multi-Session Analysis, and Structured Report Generation.

### 3. Multi-Interview Analysis & Pattern Identification
- **Implemented**:
  - Per-question scoring (0-10), strengths, weaknesses, missing concepts, feedback (`app/analysis/scoring.py`).
- **Missing**:
  - `app/analysis/comparison.py` is currently empty (0 bytes).
  - `app/analysis/weakness.py` is an un-implemented stub.
  - Aggregation of repeated wrong answers, recurring technical gaps across last $N$ interviews, communication/problem-solving trends, and priority "Topics to Work On".

### 4. Candidate Analysis API & Query Interface
- **Implemented**:
  - Basic FastAPI endpoints (`/health`, `/pipeline/run`, `/search`, `/stats`, `/chunks`).
- **Missing**:
  - `/api/v1/candidate/analyze` endpoint to execute the LangGraph pipeline for queries like *"What are Samiksha's main weaknesses across her last 3 interviews?"*.

---

## User Review Required

> [!IMPORTANT]
> **No code was modified in this session.** The implementation plan below details the exact modular changes required to reach full feature completion.

> [!NOTE]
> **Candidate Identification**: Transcripts in S3 use numeric `user_id`s in path prefixes (e.g. `simulation_training/2071/...`). Should we add a `candidate_name` field to the S3 metadata / mapping file, or pass candidate name to user ID mappings in config?

---

## Proposed Technical Changes

### Phase 1: Candidate Metadata & S3 Multi-Session Retrieval
Expand metadata extraction and S3 services to support fetching candidate history across multiple interviews.

#### [NEW] [candidate_service.py](file:///e:/interview-intelligence-rag/backend/app/services/candidate_service.py)
- Resolves candidate names (e.g., `"Samiksha"`) to `user_id` (or vice-versa).
- Fetches the candidate's last $N$ interview sessions sorted by `session_start_time`.

#### [MODIFY] [s3_service.py](file:///e:/interview-intelligence-rag/backend/app/services/s3_service.py)
- Add `get_latest_candidate_transcripts(user_id: str, limit: int = 3)` to fetch raw full transcripts directly from S3 for a candidate's previous sessions.

---

### Phase 2: Multi-Interview Comparison & Pattern Detection Engine
Build the core engine for cross-session pattern recognition and trend analysis.

#### [NEW] [comparison.py](file:///e:/interview-intelligence-rag/backend/app/analysis/comparison.py)
- `compare_interviews(session_records_list: list[list[dict]])`:
  - Identifies **Repeated Wrong Answers** (questions/topics failed in $>1$ session).
  - Detects **Recurring Technical Gaps** (missing concepts appearing across multiple interviews).
  - Evaluates **Communication & Problem-Solving Trends** over time.
  - Generates prioritized **Topics to Work On**.

#### [NEW] [report_generator.py](file:///e:/interview-intelligence-rag/backend/app/analysis/report_generator.py)
- Synthesizes session analyses into a structured Candidate Performance Report.

---

### Phase 3: LangGraph Pipeline Orchestration
Build the complete state-driven LangGraph workflow.

#### [NEW] [agent_state.py](file:///e:/interview-intelligence-rag/backend/app/graph/agent_state.py)
- Define `CandidateAnalysisState` TypedDict:
  - `query`: User query text (e.g., *"What are Samiksha's main weaknesses across her last 3 interviews?"*)
  - `candidate_name` / `user_id`: Target candidate
  - `num_interviews`: Number of recent interviews to analyze (default: 3)
  - `sessions_metadata`: Retrieved metadata for sessions
  - `rag_chunks`: Vector search chunks retrieved from ChromaDB
  - `full_transcripts`: Raw transcripts from S3
  - `multi_interview_analysis`: Aggregated pattern findings
  - `final_report`: Structured output response

#### [NEW] [nodes.py](file:///e:/interview-intelligence-rag/backend/app/graph/nodes.py)
1. `understand_query_node`: Extracts candidate name, intent, and number of interviews requested from user prompt using LLM.
2. `retrieve_sessions_node`: Queries ChromaDB and S3 for the candidate's latest $N$ interview sessions.
3. `rag_retrieval_node`: Retrieves semantically relevant Q&A chunks for targeted query topics.
4. `analyze_patterns_node`: Calls `comparison.py` engine to extract weakness patterns, repeated errors, and knowledge gaps.
5. `generate_report_node`: Constructs the final structured performance report.

#### [NEW] [workflow.py](file:///e:/interview-intelligence-rag/backend/app/graph/workflow.py)
- Compiles the nodes into a executable LangGraph `StateGraph`.

---

### Phase 4: API Integration & Frontend UI

#### [MODIFY] [routes.py](file:///e:/interview-intelligence-rag/backend/app/api/routes.py)
- Add `POST /api/v1/candidate/analyze` endpoint accepting query and returning structured analysis from the LangGraph graph.

#### [NEW] [CandidateAnalysisPage.jsx](file:///e:/interview-intelligence-rag/frontend/src/pages/CandidateAnalysisPage.jsx)
- Frontend UI tab allowing recruiters/evaluators to input natural language queries like *"What are Samiksha's main weaknesses across her last 3 interviews?"* and render interactive performance visualizers, topic radar charts, and pattern cards.

---

## Verification Plan

### Automated Tests
1. **S3 Multi-Session Retrieval Test**:
   - `pytest backend/test_s3_multi_session.py` to verify retrieving candidate's last $N$ sessions from S3.
2. **Comparison Engine Test**:
   - `pytest backend/test_comparison_engine.py` with mock 3-session transcript data to verify pattern detection for repeated wrong answers and recurring technical gaps.
3. **LangGraph Pipeline Test**:
   - `pytest backend/test_langgraph_pipeline.py` to verify end-to-end execution of the state graph with candidate query input.

### Manual Verification
1. Run backend server: `uvicorn app.main:app --reload` inside `backend`.
2. Post test request to `/api/v1/candidate/analyze` with payload:
   ```json
   {
     "query": "What are Samiksha's main weaknesses across her last 3 interviews?",
     "candidate_name": "Samiksha",
     "num_interviews": 3
   }
   ```
3. Inspect output report for recurring weaknesses, repeated incorrect answers, knowledge gaps, and recommended improvement topics.
