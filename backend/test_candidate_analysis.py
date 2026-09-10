from unittest.mock import MagicMock
from app.analysis.comparison import MultiInterviewAnalyzer
from app.analysis.report_generator import ReportGenerator
from app.analysis.weakness import aggregate_weakness_patterns


def test_weakness_aggregation():
    sample_records_session_1 = [
        {
            "question_id": "q1",
            "question": "Explain vector embeddings",
            "score": 8,
            "topic": "Embeddings & vector similarity",
            "subtopic": "Embeddings",
            "weaknesses": [],
            "missing_concepts": [],
            "counts_toward_score": True,
        },
        {
            "question_id": "q2",
            "question": "What is BPE tokenisation?",
            "score": 4,
            "topic": "Tokenisation fundamentals",
            "subtopic": "BPE tokenisation",
            "weaknesses": ["Confused subword merging with character level"],
            "missing_concepts": ["Vocabulary merge rules", "Byte-pair encoding step"],
            "counts_toward_score": True,
        },
    ]

    sample_records_session_2 = [
        {
            "question_id": "q3",
            "question": "How does BPE tokenisation work?",
            "score": 3,
            "topic": "Tokenisation fundamentals",
            "subtopic": "BPE tokenisation",
            "weaknesses": ["Struggled to explain vocabulary merge steps"],
            "missing_concepts": ["Vocabulary merge rules", "Frequency pairing"],
            "counts_toward_score": True,
        }
    ]

    result = aggregate_weakness_patterns([sample_records_session_1, sample_records_session_2])
    print("Aggregate weakness result:", result)

    assert result["total_questions_evaluated"] == 3
    assert len(result["repeated_wrong_answers"]) == 2
    assert any(g["concept"] == "Vocabulary merge rules" for g in result["recurring_technical_gaps"])
    print("[OK] test_weakness_aggregation PASSED")


def test_multi_interview_analyzer():
    analyzer = MultiInterviewAnalyzer()

    mock_session_1 = {
        "session_id": "sess_001",
        "session_start_time": "2026-01-01T10:00:00Z",
        "results": [
            {"score": 6, "topic": "Vector DB", "subtopic": "Chroma", "counts_toward_score": True, "weaknesses": ["Shallow explanation"], "missing_concepts": ["HNSW index"]}
        ]
    }

    mock_session_2 = {
        "session_id": "sess_002",
        "session_start_time": "2026-02-01T10:00:00Z",
        "results": [
            {"score": 8, "topic": "Vector DB", "subtopic": "Chroma", "counts_toward_score": True, "weaknesses": [], "missing_concepts": []}
        ]
    }

    analysis = analyzer.analyze_candidate_history("Samiksha", "2071", [mock_session_2, mock_session_1])
    print("Multi-Interview Analysis:", analysis)

    assert analysis["candidate_name"] == "Samiksha"
    assert analysis["user_id"] == "2071"
    assert analysis["sessions_analyzed"] == 2
    assert analysis["overall_average_score"] == 7.0
    print("[OK] test_multi_interview_analyzer PASSED")


def test_report_generator():
    mock_analysis = {
        "candidate_name": "Samiksha",
        "user_id": "2071",
        "sessions_analyzed": 2,
        "overall_average_score": 7.5,
        "performance_trend": "improving",
        "recurring_technical_gaps": [{"concept": "Vocabulary merge rules", "occurrence_count": 2}],
        "topics_to_improve": [{"topic": "Tokenisation fundamentals", "error_count": 2, "avg_score": 3.5}],
        "top_weaknesses": ["Subword tokenisation details"],
    }

    mock_llm = MagicMock()
    mock_llm.generate.return_value = "Executive Summary: Candidate Samiksha demonstrated strong improvement across her recent interviews."

    generator = ReportGenerator(llm_service=mock_llm)
    report = generator.generate_report(mock_analysis, user_query="What are Samiksha's main weaknesses?")

    print("Report Generator Output:", report)
    assert report["candidate_name"] == "Samiksha"
    assert report["overall_score"] == 7.5
    assert "Executive Summary" in report["executive_summary"]
    print("[OK] test_report_generator PASSED")


if __name__ == "__main__":
    test_weakness_aggregation()
    test_multi_interview_analyzer()
    test_report_generator()
    print("All multi-interview analysis tests passed successfully!")
