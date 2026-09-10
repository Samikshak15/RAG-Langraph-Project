/**
 * @typedef {"local" | "s3_latest"} PipelineSource
 *
 * @typedef {Object} QuestionResult
 * @property {string} question_id
 * @property {number} question_turn
 * @property {number[]} answer_turns
 * @property {string} question
 * @property {string} answer
 * @property {string} topic
 * @property {string} subtopic
 * @property {number} score
 * @property {string[]} strengths
 * @property {string[]} weaknesses
 * @property {string[]} missing_concepts
 * @property {string} feedback
 * @property {boolean} counts_toward_score
 *
 * @typedef {Object} PipelineSummary
 * @property {number} total_questions
 * @property {number} scored_questions
 * @property {number} not_covered_questions
 * @property {number} average_score
 * @property {string[]} topics_covered
 *
 * @typedef {Object} PipelineRunResponse
 * @property {string} session_id
 * @property {string} user_id
 * @property {string} bot_id
 * @property {string} source_key
 * @property {string|null} session_start_time
 * @property {QuestionResult[]} results
 * @property {PipelineSummary} summary
 * @property {number} chunks_stored
 * @property {number} collection_count
 *
 * @typedef {Object} SearchResult
 * @property {string} chunk_id
 * @property {string} text
 * @property {number} distance
 * @property {number} rerank_score
 * @property {string} session_id
 * @property {string} user_id
 * @property {string} question_id
 * @property {string} question
 * @property {string} answer
 * @property {string} topic
 * @property {string} subtopic
 * @property {number} score
 * @property {string[]} strengths
 * @property {string[]} weaknesses
 * @property {string[]} missing_concepts
 * @property {string} feedback
 * @property {boolean} counts_toward_score
 *
 * @typedef {Object} SearchResponse
 * @property {string} query
 * @property {SearchResult[]} results
 *
 * @typedef {Object} HealthResponse
 * @property {"ok"} status
 * @property {number} chroma_collection_count
 *
 * @typedef {Object} ChunkListItem
 * @property {string} chunk_id
 * @property {string} question_id
 * @property {string} session_id
 * @property {string} topic
 * @property {string} subtopic
 * @property {number} score
 * @property {boolean} counts_toward_score
 * @property {string|null} stored_at
 *
 * @typedef {Object} ChunkListResponse
 * @property {ChunkListItem[]} chunks
 * @property {number} total
 * @property {number} limit
 * @property {number} offset
 *
 * @typedef {Object} StatsResponse
 * @property {number} total_chunks
 * @property {number} distinct_sessions
 * @property {number} avg_score
 * @property {number} vector_store_bytes
 * @property {string|null} last_stored_at
 */
export {};
