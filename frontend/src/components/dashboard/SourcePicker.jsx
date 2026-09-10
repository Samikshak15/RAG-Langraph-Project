import Button from "@mui/material/Button";
import Paper from "@mui/material/Paper";
import Stack from "@mui/material/Stack";
import ToggleButton from "@mui/material/ToggleButton";
import ToggleButtonGroup from "@mui/material/ToggleButtonGroup";
import Typography from "@mui/material/Typography";
import PlayArrowIcon from "@mui/icons-material/PlayArrow";
import { useState } from "react";

export default function SourcePicker({ disabled, onRun }) {
  const [source, setSource] = useState("local");

  return (
    <Paper variant="outlined" sx={{ p: 3, mb: 3 }}>
      <Typography variant="subtitle1" fontWeight={600} gutterBottom>
        1. Choose a transcript
      </Typography>
      <Stack direction={{ xs: "column", sm: "row" }} spacing={2} sx={{ alignItems: { sm: "center" } }}>
        <ToggleButtonGroup
          value={source}
          exclusive
          onChange={(_, value) => value && setSource(value)}
          size="small"
          disabled={disabled}
        >
          <ToggleButton value="local">Local sample transcript</ToggleButton>
          <ToggleButton value="s3_latest">Latest transcript from S3</ToggleButton>
        </ToggleButtonGroup>

        <Button
          variant="contained"
          startIcon={<PlayArrowIcon />}
          disabled={disabled}
          onClick={() => onRun(source)}
        >
          Run full pipeline
        </Button>
      </Stack>
      <Typography variant="caption" color="text.secondary" sx={{ mt: 1.5, display: "block" }}>
        Runs: fetch → parse → Q&amp;A extraction → topic classification → answer evaluation →
        enrichment → chunking → embedding → ChromaDB storage.
      </Typography>
    </Paper>
  );
}
