import Chip from "@mui/material/Chip";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
import { getRunHistory } from "../../utils/runHistory";

// Topics come from the most recently completed run's real topics_covered
// when available. Otherwise these are clearly example queries, not a claim
// of real topic data — matches the existing placeholder-text precedent.
const EXAMPLE_QUERIES = ["How do you evaluate RAG retrieval quality?", "Why use chunking in RAG?"];

export default function SuggestedChips({ onPick }) {
  const lastCompleted = getRunHistory().find((run) => run.status === "completed" && run.response);
  const topics = lastCompleted?.response?.summary?.topics_covered ?? [];

  const items = topics.length > 0 ? topics : EXAMPLE_QUERIES;
  const label = topics.length > 0 ? "Topics from your last run:" : "Try:";

  return (
    <Stack direction="row" spacing={1} useFlexGap sx={{ alignItems: "center", flexWrap: "wrap", mb: 3 }}>
      <Typography variant="caption" color="text.secondary">
        {label}
      </Typography>
      {items.map((item) => (
        <Chip key={item} label={item} size="small" variant="outlined" onClick={() => onPick(item)} />
      ))}
    </Stack>
  );
}
