import CheckIcon from "@mui/icons-material/Check";
import ErrorOutlineIcon from "@mui/icons-material/ErrorOutlineOutlined";
import Box from "@mui/material/Box";
import CircularProgress from "@mui/material/CircularProgress";
import Paper from "@mui/material/Paper";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";

const STEPS = [
  "Transcript Parsed",
  "Q&A Extracted",
  "Metadata Extracted",
  "Topic Classified",
  "Answers Evaluated",
  "Enriched Records",
  "Chunks Built",
  "Embeddings Gen.",
  "Stored ChromaDB",
];

// Elapsed-time heuristic for which step is "active" — NOT real backend
// progress events (the API call is a single synchronous request/response,
// per this project's deliberate v1 design). Classification + evaluation
// dominate total runtime (2 sequential LLM calls per question), so most
// of the timeline is spent on those two steps.
const STAGE_BOUNDS_SECONDS = [3, 5, 6, 50, 90, 93, 95, 100, Infinity];

export function activeStepIndex(elapsedSeconds) {
  const index = STAGE_BOUNDS_SECONDS.findIndex((bound) => elapsedSeconds < bound);
  return index === -1 ? STEPS.length - 1 : index;
}

function StepBadge({ label, state }) {
  // state: "done" | "active" | "pending" | "error"
  const styles = {
    done: { bg: "#e6f7ec", color: "#1e9e5a", border: "#bdead0" },
    active: { bg: "primary.main", color: "#fff", border: "primary.main" },
    pending: { bg: "#f2f0f8", color: "#9c94b5", border: "#e3ddf0" },
    error: { bg: "#fdeaea", color: "#d32f2f", border: "#f5c2c2" },
  }[state];

  return (
    <Stack spacing={0.75} sx={{ alignItems: "center", minWidth: 76 }}>
      <Box
        sx={{
          width: 34,
          height: 34,
          borderRadius: "50%",
          bgcolor: styles.bg,
          border: `1px solid ${styles.border}`,
          color: styles.color,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        {state === "done" && <CheckIcon fontSize="small" />}
        {state === "active" && <CircularProgress size={16} sx={{ color: "#fff" }} />}
        {state === "error" && <ErrorOutlineIcon fontSize="small" />}
      </Box>
      <Typography variant="caption" align="center" color="text.secondary" sx={{ lineHeight: 1.2 }}>
        {label}
      </Typography>
    </Stack>
  );
}

export default function PipelineStepper({ status, elapsedSeconds }) {
  const isSuccess = status === "success";
  const isError = status === "error";
  const activeIndex = activeStepIndex(elapsedSeconds);

  return (
    <Paper variant="outlined" sx={{ p: 3, mb: 3 }}>
      <Typography variant="subtitle1" fontWeight={600} sx={{ mb: 2.5 }}>
        Current RAG Ingestion Pipeline
      </Typography>

      <Stack direction="row" spacing={1} useFlexGap sx={{ justifyContent: "space-between", flexWrap: "wrap" }}>
        {STEPS.map((label, index) => {
          let state = "pending";
          if (status === "loading") {
            if (index < activeIndex) state = "done";
            else if (index === activeIndex) state = "active";
          } else if (isSuccess) {
            state = "done";
          } else if (isError) {
            if (index < activeIndex) state = "done";
            else if (index === activeIndex) state = "error";
          }

          return <StepBadge key={label} label={label} state={state} />;
        })}
      </Stack>

      {!isSuccess && !isError && status === "loading" && (
        <Typography variant="caption" color="text.secondary" sx={{ mt: 2, display: "block" }}>
          {elapsedSeconds}s elapsed — typically 60-90s for an 11-question transcript (each
          question makes two sequential LLM calls: classification, then evaluation).
        </Typography>
      )}
    </Paper>
  );
}
