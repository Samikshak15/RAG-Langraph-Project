import Alert from "@mui/material/Alert";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Snackbar from "@mui/material/Snackbar";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
import BadgeOutlinedIcon from "@mui/icons-material/BadgeOutlined";
import CalendarTodayOutlinedIcon from "@mui/icons-material/CalendarTodayOutlined";
import { useState } from "react";
import CandidateAnalysisCard from "../components/candidates/CandidateAnalysisCard";
import CandidateRAGPanel from "../components/candidates/CandidateRAGPanel";
import CandidateSelector from "../components/candidates/CandidateSelector";
import { ingestCandidateTranscripts } from "../api/candidates";

export default function CandidateHubPage() {
  const [selectedCandidate, setSelectedCandidate] = useState(null);
  const [ingestLoading, setIngestLoading] = useState(false);
  const [toast, setToast] = useState({ open: false, message: "", severity: "info" });

  const handleIngest = async (userId) => {
    if (!userId) return;
    setIngestLoading(true);
    try {
      const res = await ingestCandidateTranscripts(userId, 3);
      setToast({
        open: true,
        message: `S3 Transcript Ingestion Complete: Processed ${res.sessions_processed || 0} session(s), stored ${res.chunks_stored || 0} vector chunk(s).`,
        severity: "success",
      });
    } catch (err) {
      setToast({
        open: true,
        message: err.message || "S3 Transcript Ingestion failed",
        severity: "error",
      });
    } finally {
      setIngestLoading(false);
    }
  };

  return (
    <Box sx={{ maxWidth: 1400, mx: "auto", pb: 6 }}>
      <Stack
        direction={{ xs: "column", sm: "row" }}
        sx={{ justifyContent: "space-between", alignItems: { sm: "center" }, mb: 3 }}
      >
        <Stack direction="row" alignItems="center" spacing={1.5}>
          <Box sx={{ p: 1, borderRadius: 2, bgcolor: "primary.main", color: "#ffffff" }}>
            <BadgeOutlinedIcon />
          </Box>
          <Box>
            <Typography variant="h5" fontWeight={700}>
              Candidate Intelligence Hub
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Interactive candidate selection, natural language RAG Q&A engine, and multi-interview performance reports.
            </Typography>
          </Box>
        </Stack>

        <Button variant="outlined" size="small" startIcon={<CalendarTodayOutlinedIcon fontSize="small" />}>
          All Active Candidates
        </Button>
      </Stack>

      <CandidateSelector
        selectedCandidate={selectedCandidate}
        onSelectCandidate={setSelectedCandidate}
        onIngestTranscripts={handleIngest}
        ingestLoading={ingestLoading}
      />

      <CandidateRAGPanel selectedCandidate={selectedCandidate} />

      <CandidateAnalysisCard selectedCandidate={selectedCandidate} />

      <Snackbar
        open={toast.open}
        autoHideDuration={6000}
        onClose={() => setToast({ ...toast, open: false })}
        anchorOrigin={{ vertical: "bottom", horizontal: "right" }}
      >
        <Alert
          onClose={() => setToast({ ...toast, open: false })}
          severity={toast.severity}
          variant="filled"
          sx={{ width: "100%", borderRadius: 2 }}
        >
          {toast.message}
        </Alert>
      </Snackbar>
    </Box>
  );
}
