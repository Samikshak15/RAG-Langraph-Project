import Accordion from "@mui/material/Accordion";
import AccordionDetails from "@mui/material/AccordionDetails";
import AccordionSummary from "@mui/material/AccordionSummary";
import Alert from "@mui/material/Alert";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Chip from "@mui/material/Chip";
import CircularProgress from "@mui/material/CircularProgress";
import Divider from "@mui/material/Divider";
import Stack from "@mui/material/Stack";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import AutoAwesomeIcon from "@mui/icons-material/AutoAwesome";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import HelpOutlineOutlinedIcon from "@mui/icons-material/HelpOutlineOutlined";
import MenuBookOutlinedIcon from "@mui/icons-material/MenuBookOutlined";
import SendIcon from "@mui/icons-material/Send";
import { useState } from "react";
import { queryCandidateRAG } from "../../api/candidates";

const PRESET_QUICK_CHIPS = [
  "Technical Weaknesses",
  "Score Trajectory & Strengths",
  "Missing Concepts in Interviews",
  "Multi-Agent System Architecture",
];

export default function CandidateRAGPanel({ selectedCandidate }) {
  const [queryText, setQueryText] = useState("");
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);
  const [expandedTurn, setExpandedTurn] = useState(false);

  const handleQuery = async (customQuery = null) => {
    const q = customQuery || queryText;
    if (!q.trim() || !selectedCandidate) return;

    setLoading(true);
    setError(null);
    try {
      const candId = selectedCandidate.user_id;
      const res = await queryCandidateRAG(candId, q, 5);
      setResponse(res);
    } catch (err) {
      setError(err.message || "RAG Q&A query failed");
    } finally {
      setLoading(false);
    }
  };

  const handleChipClick = (chipText) => {
    const fullQuery = `What are the candidate's ${chipText.toLowerCase()} across recent interviews?`;
    setQueryText(fullQuery);
    handleQuery(fullQuery);
  };

  const getScoreColor = (score) => {
    if (score >= 8) return "success";
    if (score >= 5) return "warning";
    return "error";
  };

  return (
    <Card sx={{ mb: 3, borderRadius: 3, boxShadow: "0 4px 20px rgba(0,0,0,0.05)", border: "1px solid #eef0f4" }}>
      <CardContent sx={{ p: 3 }}>
        <Stack direction="row" alignItems="center" spacing={1.5} sx={{ mb: 2 }}>
          <Box sx={{ p: 1, borderRadius: 2, bgcolor: "#f3e8ff", color: "#7e22ce" }}>
            <AutoAwesomeIcon />
          </Box>
          <Box>
            <Typography variant="h6" fontWeight={700}>
              Candidate RAG Q&A Engine
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Ask natural language questions about candidate performance. Evidence is retrieved from isolated vector search.
            </Typography>
          </Box>
        </Stack>

        <Stack spacing={2} sx={{ mb: 3 }}>
          <Stack direction={{ xs: "column", sm: "row" }} spacing={1.5}>
            <TextField
              fullWidth
              variant="outlined"
              size="small"
              placeholder={
                selectedCandidate
                  ? `Ask a question about ${selectedCandidate.name} (e.g. What are main weaknesses in vector DBs?)...`
                  : "Select a candidate above to ask questions..."
              }
              value={queryText}
              onChange={(e) => setQueryText(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleQuery()}
              disabled={!selectedCandidate || loading}
              sx={{ "& .MuiOutlinedInput-root": { borderRadius: 2 } }}
            />
            <Button
              variant="contained"
              color="primary"
              disabled={!selectedCandidate || !queryText.trim() || loading}
              onClick={() => handleQuery()}
              endIcon={loading ? <CircularProgress size={16} color="inherit" /> : <SendIcon />}
              sx={{ minWidth: 140, borderRadius: 2, textTransform: "none", fontWeight: 600 }}
            >
              {loading ? "Synthesizing..." : "Ask AI Engine"}
            </Button>
          </Stack>

          <Stack direction="row" spacing={1} alignItems="center" flexWrap="wrap" gap={0.5}>
            <Typography variant="caption" color="text.secondary" fontWeight={600}>
              Quick Presets:
            </Typography>
            {PRESET_QUICK_CHIPS.map((chip) => (
              <Chip
                key={chip}
                label={chip}
                size="small"
                clickable
                disabled={!selectedCandidate || loading}
                onClick={() => handleChipClick(chip)}
                sx={{
                  bgcolor: "#f1f5f9",
                  fontSize: 12,
                  fontWeight: 500,
                  "&:hover": { bgcolor: "#e2e8f0" },
                }}
              />
            ))}
          </Stack>
        </Stack>

        {error && (
          <Alert severity="error" sx={{ mb: 3, borderRadius: 2 }}>
            {error}
          </Alert>
        )}

        {response && (
          <Box sx={{ mt: 3 }}>
            <Card variant="outlined" sx={{ borderRadius: 2.5, bgcolor: "#fafafa", mb: 3 }}>
              <CardContent sx={{ p: 3 }}>
                <Stack direction="row" alignItems="center" justifyContent="space-between" sx={{ mb: 2 }}>
                  <Stack direction="row" spacing={1} alignItems="center">
                    <AutoAwesomeIcon color="primary" fontSize="small" />
                    <Typography variant="subtitle2" fontWeight={700} color="primary.main">
                      AI Synthesized Answer for {response.candidate_name}
                    </Typography>
                  </Stack>
                  <Chip
                    label={`${response.sources_retrieved_count} Source Turns Cited`}
                    size="small"
                    color="secondary"
                    variant="outlined"
                    sx={{ fontSize: 11, height: 22 }}
                  />
                </Stack>

                <Typography
                  variant="body1"
                  sx={{
                    whiteSpace: "pre-line",
                    lineHeight: 1.7,
                    color: "#1e293b",
                    fontFamily: "Inter, Roboto, sans-serif",
                    "& h3, & h4": { fontWeight: 700, mt: 2, mb: 1 },
                    "& ul": { pl: 2.5, my: 1 },
                  }}
                >
                  {response.answer}
                </Typography>
              </CardContent>
            </Card>

            {response.sources && response.sources.length > 0 && (
              <Box>
                <Typography variant="subtitle2" fontWeight={700} color="text.secondary" sx={{ mb: 1.5, display: "flex", alignItems: "center", gap: 1 }}>
                  <MenuBookOutlinedIcon fontSize="small" />
                  Retrieved Vector Evidence Turns ({response.sources.length})
                </Typography>

                <Stack spacing={1.5}>
                  {response.sources.map((source, i) => (
                    <Accordion
                      key={source.chunk_id || i}
                      expanded={expandedTurn === i}
                      onChange={(_, isExpanded) => setExpandedTurn(isExpanded ? i : false)}
                      sx={{
                        borderRadius: "8px !important",
                        border: "1px solid #e2e8f0",
                        boxShadow: "none",
                        "&:before": { display: "none" },
                      }}
                    >
                      <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                        <Stack direction="row" alignItems="center" spacing={2} sx={{ width: "100%", pr: 2 }}>
                          <Chip
                            label={`${source.score ?? 0}/10`}
                            color={getScoreColor(source.score ?? 0)}
                            size="small"
                            sx={{ fontWeight: 700, minWidth: 50 }}
                          />
                          <Box sx={{ flexGrow: 1, minWidth: 0 }}>
                            <Typography variant="body2" fontWeight={600} noWrap>
                              {source.question || "Interview Question"}
                            </Typography>
                            <Typography variant="caption" color="text.secondary">
                              Topic: {source.topic} • Subtopic: {source.subtopic}
                            </Typography>
                          </Box>
                          {source.rerank_score && (
                            <Chip
                              label={`Rerank: ${Number(source.rerank_score).toFixed(2)}`}
                              size="small"
                              variant="outlined"
                              sx={{ fontSize: 10, height: 20 }}
                            />
                          )}
                        </Stack>
                      </AccordionSummary>

                      <AccordionDetails sx={{ bgcolor: "#f8fafc", pt: 1, borderTop: "1px solid #f1f5f9" }}>
                        <Stack spacing={1.5}>
                          <Box>
                            <Typography variant="caption" fontWeight={700} color="text.secondary">
                              CANDIDATE ANSWER:
                            </Typography>
                            <Typography variant="body2" sx={{ bgcolor: "#ffffff", p: 1.5, borderRadius: 1.5, border: "1px solid #e2e8f0", mt: 0.5 }}>
                              {source.answer}
                            </Typography>
                          </Box>

                          <Stack direction={{ xs: "column", sm: "row" }} spacing={2}>
                            {source.weaknesses && source.weaknesses.length > 0 && (
                              <Box sx={{ flex: 1 }}>
                                <Typography variant="caption" fontWeight={700} color="error.main">
                                  Weaknesses:
                                </Typography>
                                <Typography variant="caption" component="div" color="text.secondary">
                                  {source.weaknesses.join(", ")}
                                </Typography>
                              </Box>
                            )}

                            {source.missing_concepts && source.missing_concepts.length > 0 && (
                              <Box sx={{ flex: 1 }}>
                                <Typography variant="caption" fontWeight={700} color="warning.main">
                                  Missing Concepts:
                                </Typography>
                                <Typography variant="caption" component="div" color="text.secondary">
                                  {source.missing_concepts.join(", ")}
                                </Typography>
                              </Box>
                            )}
                          </Stack>

                          {source.feedback && (
                            <Box sx={{ pt: 0.5 }}>
                              <Typography variant="caption" fontWeight={700} color="primary.main">
                                Evaluation Feedback:
                              </Typography>
                              <Typography variant="caption" component="div" color="text.secondary">
                                {source.feedback}
                              </Typography>
                            </Box>
                          )}
                        </Stack>
                      </AccordionDetails>
                    </Accordion>
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
