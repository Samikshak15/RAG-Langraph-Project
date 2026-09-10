from typing import Any
from app.analysis.weakness import aggregate_weakness_patterns


class MultiInterviewAnalyzer:
    """
    Analyzes and compares candidate performance across multiple interview sessions.
    """

    def analyze_candidate_history(
        self, candidate_name: str, user_id: str, sessions_data: list[dict]
    ) -> dict[str, Any]:
        """
        Input:
            candidate_name: Candidate display name (e.g. "Samiksha")
            user_id: Candidate numeric user ID (e.g. "2071")
            sessions_data: list of dicts, each representing a session with "session_id",
                          "session_start_time", and "results" (evaluated Q&A records).
        """
        if not sessions_data:
            return {
                "candidate_name": candidate_name,
                "user_id": user_id,
                "sessions_analyzed": 0,
                "summary": "No completed interview sessions found for this candidate.",
            }

        session_summaries = []
        all_session_records = []

        for s in sessions_data:
            records = s.get("results", [])
            all_session_records.append(records)

            scored = [r for r in records if r.get("counts_toward_score", True)]
            avg_score = (
                round(sum(r.get("score", 0) for r in scored) / len(scored), 2)
                if scored
                else 0.0
            )

            session_summaries.append({
                "session_id": s.get("session_id"),
                "session_start_time": s.get("session_start_time"),
                "total_questions": len(records),
                "average_score": avg_score,
                "topics_covered": sorted({r.get("topic", "general") for r in scored}),
            })

        # Calculate score trend across sessions (chronological order)
        scores = [s["average_score"] for s in session_summaries]
        overall_avg = round(sum(scores) / len(scores), 2) if scores else 0.0

        if len(scores) >= 2:
            diff = scores[0] - scores[-1]  # session_summaries are newest-first
            if diff > 0.5:
                trend = "improving"
            elif diff < -0.5:
                trend = "regressing"
            else:
                trend = "stable"
        else:
            trend = "single_session"

        # Aggregate weakness patterns & recurring technical gaps
        weakness_patterns = aggregate_weakness_patterns(all_session_records)

        return {
            "candidate_name": candidate_name,
            "user_id": user_id,
            "sessions_analyzed": len(sessions_data),
            "overall_average_score": overall_avg,
            "performance_trend": trend,
            "session_summaries": session_summaries,
            "repeated_wrong_answers": weakness_patterns["repeated_wrong_answers"],
            "recurring_technical_gaps": weakness_patterns["recurring_technical_gaps"],
            "topics_to_improve": weakness_patterns["topics_to_improve"],
            "top_weaknesses": [w[0] for w in weakness_patterns["top_weaknesses"]],
        }
