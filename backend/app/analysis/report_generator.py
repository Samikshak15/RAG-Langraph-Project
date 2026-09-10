from typing import Any
from app.services.llm_service import LLMService


class ReportGenerator:
    def __init__(self, llm_service: LLMService | None = None):
        self.llm = llm_service or LLMService()

    def generate_report(self, analysis: dict[str, Any], user_query: str = "") -> dict[str, Any]:
        """
        Generates a structured candidate performance report with executive summary.
        """
        candidate_name = analysis.get("candidate_name", "Candidate")
        overall_score = analysis.get("overall_average_score", 0.0)
        trend = analysis.get("performance_trend", "stable")
        sessions_count = analysis.get("sessions_analyzed", 0)
        topics_to_improve = analysis.get("topics_to_improve", [])
        recurring_gaps = analysis.get("recurring_technical_gaps", [])

        # Executive summary template synthesis
        prompt = f"""
You are an expert technical interview panel lead writing an executive performance report.

Candidate: {candidate_name}
User Query: {user_query or "Analyze performance across recent interviews"}
Number of Sessions Analyzed: {sessions_count}
Overall Average Score: {overall_score}/10
Performance Trend: {trend}

Top Recurring Gaps: {[g['concept'] for g in recurring_gaps[:5]]}
Priority Topics to Improve: {[t['topic'] for t in topics_to_improve[:5]]}
Top Weaknesses: {analysis.get("top_weaknesses", [])[:5]}

Write a concise, professional 2-3 paragraph executive summary evaluating the candidate's performance trend, key technical gaps, communication strengths, and recommended focus areas.
"""
        try:
            executive_summary = self.llm.generate(prompt)
        except Exception:
            executive_summary = (
                f"Candidate {candidate_name} completed {sessions_count} interview session(s) "
                f"with an overall average score of {overall_score}/10 (trend: {trend}). "
                f"Key areas for improvement include: {', '.join([t['topic'] for t in topics_to_improve[:3]]) or 'General technical topics'}."
            )

        return {
            "candidate_name": candidate_name,
            "user_id": analysis.get("user_id"),
            "user_query": user_query,
            "sessions_analyzed": sessions_count,
            "overall_score": overall_score,
            "performance_trend": trend,
            "executive_summary": executive_summary,
            "session_summaries": analysis.get("session_summaries", []),
            "repeated_wrong_answers": analysis.get("repeated_wrong_answers", []),
            "recurring_technical_gaps": recurring_gaps,
            "topics_to_work_on": topics_to_improve,
        }
