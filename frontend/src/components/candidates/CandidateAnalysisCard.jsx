import Alert from "@mui/material/Alert";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Chip from "@mui/material/Chip";
import CircularProgress from "@mui/material/CircularProgress";
import Grid from "@mui/material/Grid";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
import AnalyticsOutlinedIcon from "@mui/icons-material/AnalyticsOutlined";
import ErrorOutlineOutlinedIcon from "@mui/icons-material/ErrorOutlineOutlined";
import LocalLibraryOutlinedIcon from "@mui/icons-material/LocalLibraryOutlined";
import TrendingUpIcon from "@mui/icons-material/TrendingUp";
import WarningAmberIcon from "@mui/icons-material/WarningAmber";
import { useState } from "react";
import { analyzeCandidate } from "../../api/candidates";

export default function CandidateAnalysisCard({ selectedCandidate }) {
  const [loading, setLoading] = useState(false);
  const [report, setReport] = useState(null);
  const [error, setError] = useState(null);

  const handleAnalyze = async () => {
    if (!selectedCandidate) return;
    setLoading(true);
    setError(null);
    try {
      const res = await analyzeCandidate(selectedCandidate.user_id, "What are the candidate's main weaknesses across recent interviews?", 3);
      setReport(res);
    } catch (err) {
      setError(err.message || "Failed to generate multi-interview analysis");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card sx={{ mb: 3, borderRadius: 3, boxShadow: "0 4px 20px rgba(0,0,0,0.05)", border: "1px solid #eef0f4" }}>
      <CardContent sx={{ p: 3 }}>
        <Stack direction={{ xs: "column", sm: "row" }} alignItems={{ sm: "center" }} justifyContent="space-between" spacing={2} sx={{ mb: 2 }}>
          <Stack direction="row" alignItems="center" spacing={1.5}>
            <Box sx={{ p: 1, borderRadius: 2, bgcolor: "#e0f2fe", color: "#0284c7" }}>
              <AnalyticsOutlinedIcon />
            </Box>
            <Box>
              <Typography variant="h6" fontWeight={700}>
                Multi-Interview Performance & Weakness Analysis
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Aggregates repeated wrong answers, recurring technical gaps, and topic recommendations across interviews.
              </Typography>
            </Box>
          </Stack>

          <Button
            variant="contained"
            color="secondary"
            disabled={!selectedCandidate || loading}
            onClick={handleAnalyze}
            startIcon={loading ? <CircularProgress size={16} color="inherit" /> : <AnalyticsOutlinedIcon />}
            sx={{ textTransform: "none", fontWeight: 600, borderRadius: 2, height: 40 }}
          >
            {loading ? "Generating Report..." : "Generate Analysis Report"}
          </Button>
        </Stack>

        {error && (
          <Alert severity="error" sx={{ mb: 3, borderRadius: 2 }}>
            {error}
          </Alert>
        )}

        {report && (
          <Box sx={{ mt: 3 }}>
            <Grid container spacing={2} sx={{ mb: 3 }}>
              <Grid size={{ xs: 12, sm: 4 }}>
                <Box sx={{ p: 2, borderRadius: 2, bgcolor: "#f8fafc", border: "1px solid #e2e8f0", textAlign: "center" }}>
                  <Typography variant="caption" color="text.secondary" fontWeight={600}>
                    OVERALL SCORE
                  </Typography>
                  <Typography variant="h4" fontWeight={800} color="primary.main">
                    {report.overall_score} / 10
                  </Typography>
                </Box>
              </Grid>

              <Grid size={{ xs: 12, sm: 4 }}>
                <Box sx={{ p: 2, borderRadius: 2, bgcolor: "#f8fafc", border: "1px solid #e2e8f0", textAlign: "center" }}>
                  <Typography variant="caption" color="text.secondary" fontWeight={600}>
                    PERFORMANCE TREND
                  </Typography>
                  <Typography variant="h6" fontWeight={700} color="success.main" sx={{ display: "flex", alignItems: "center", justifyContent: "center", gap: 0.5, mt: 0.5 }}>
                    <TrendingUpIcon />
                    {report.performance_trend || "Stable"}
                  </Typography>
                </Box>
              </Grid>

              <Grid size={{ xs: 12, sm: 4 }}>
                <Box sx={{ p: 2, borderRadius: 2, bgcolor: "#f8fafc", border: "1px solid #e2e8f0", textAlign: "center" }}>
                  <Typography variant="caption" color="text.secondary" fontWeight={600}>
                    SESSIONS ANALYZED
                  </Typography>
                  <Typography variant="h4" fontWeight={800} color="secondary.main">
                    {report.sessions_analyzed}
                  </Typography>
                </Box>
              </Grid>
            </Grid>

            {report.executive_summary && (
              <Box sx={{ p: 2.5, borderRadius: 2, bgcolor: "#eff6ff", border: "1px solid #bfdbfe", mb: 3 }}>
                <Typography variant="subtitle2" fontWeight={700} color="#1e40af" sx={{ mb: 0.5 }}>
                  Executive Summary
                </Typography>
                <Typography variant="body2" color="#1e3a8a" sx={{ lineHeight: 1.6 }}>
                  {report.executive_summary}
                </Typography>
              </Box>
            )}

            <Grid container spacing={3}>
              <Grid size={{ xs: 12, md: 6 }}>
                <Card variant="outlined" sx={{ borderRadius: 2, height: "100%" }}>
                  <CardContent sx={{ p: 2.5 }}>
                    <Stack direction="row" alignItems="center" spacing={1} sx={{ mb: 1.5 }}>
                      <ErrorOutlineOutlinedIcon color="error" fontSize="small" />
                      <Typography variant="subtitle2" fontWeight={700}>
                        Repeated Wrong Answers ({report.repeated_wrong_answers?.length || 0})
                      </Typography>
                    </Stack>
                    <Stack spacing={1}>
                      {report.repeated_wrong_answers && report.repeated_wrong_answers.length > 0 ? (
                        report.repeated_wrong_answers.map((item, idx) => (
                          <Box key={idx} sx={{ p: 1.5, borderRadius: 1.5, bgcolor: "#fef2f2", border: "1px solid #fee2e2" }}>
                            <Typography variant="body2" fontWeight={600} color="error.main">
                              {item.question || item.topic}
                            </Typography>
                            <Typography variant="caption" color="text.secondary">
                              Topic: {item.topic} • Score: {item.score}/10
                            </Typography>
                          </Box>
                        ))
                      ) : (
                        <Typography variant="caption" color="text.secondary">
                          No repeated wrong answers detected across recent interviews.
                        </Typography>
                      )}
                    </Stack>
                  </CardContent>
                </Card>
              </Grid>

              <Grid size={{ xs: 12, md: 6 }}>
                <Card variant="outlined" sx={{ borderRadius: 2, height: "100%" }}>
                  <CardContent sx={{ p: 2.5 }}>
                    <Stack direction="row" alignItems="center" spacing={1} sx={{ mb: 1.5 }}>
                      <WarningAmberIcon color="warning" fontSize="small" />
                      <Typography variant="subtitle2" fontWeight={700}>
                        Recurring Technical Gaps ({report.recurring_technical_gaps?.length || 0})
                      </Typography>
                    </Stack>
                    <Stack spacing={1}>
                      {report.recurring_technical_gaps && report.recurring_technical_gaps.length > 0 ? (
                        report.recurring_technical_gaps.map((item, idx) => (
                          <Box key={idx} sx={{ p: 1.5, borderRadius: 1.5, bgcolor: "#fffbebe", border: "1px solid #fef3c7" }}>
                            <Typography variant="body2" fontWeight={600} color="#b45309">
                              {item.concept || item.topic}
                            </Typography>
                            <Typography variant="caption" color="text.secondary">
                              Occurrence: {item.frequency || "Multiple interviews"}
                            </Typography>
                          </Box>
                        ))
                      ) : (
                        <Typography variant="caption" color="text.secondary">
                          No recurring gaps detected. Candidate demonstrated consistent topic understanding.
                        </Typography>
                      )}
                    </Stack>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>

            {report.topics_to_work_on && report.topics_to_work_on.length > 0 && (
              <Box sx={{ mt: 3, p: 2.5, borderRadius: 2, bgcolor: "#f8fafc", border: "1px solid #e2e8f0" }}>
                <Stack direction="row" alignItems="center" spacing={1} sx={{ mb: 1.5 }}>
                  <LocalLibraryOutlinedIcon color="primary" fontSize="small" />
                  <Typography variant="subtitle2" fontWeight={700}>
                    Recommended Topics to Improve
                  </Typography>
                </Stack>
                <Stack direction="row" spacing={1} flexWrap="wrap" gap={1}>
                  {report.topics_to_work_on.map((topic, idx) => (
                    <Chip
                      key={idx}
                      label={typeof topic === "string" ? topic : topic.topic || topic.name}
                      color="primary"
                      variant="outlined"
                      sx={{ fontWeight: 600 }}
                    />
                  ))}
                </Stack>
              </Box>
            )}
          </Box>
        )}
      </CardContent>
    </Card>
  );
}
