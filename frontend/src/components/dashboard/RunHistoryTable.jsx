import Box from "@mui/material/Box";
import LinearProgress from "@mui/material/LinearProgress";
import Paper from "@mui/material/Paper";
import Stack from "@mui/material/Stack";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import { activeStepIndex } from "./PipelineStepper";

const PIPELINE_STEP_COUNT = 9; // must match PipelineStepper.jsx's STEPS length

const SOURCE_LABEL = {
  local: "Local sample transcript",
  s3_latest: "Latest from S3",
};

const STATUS_STYLE = {
  loading: { label: "Processing", dot: "#0ea5e9", text: "#0369a1" },
  completed: { label: "Completed", dot: "#22c55e", text: "#15803d" },
  failed: { label: "Failed", dot: "#ef4444", text: "#b91c1c" },
};

// Completed = 100% is factually accurate (the run really did finish every
// stage). For an in-progress or failed run, the percentage is the same
// elapsed-time heuristic used for the live stepper — an honest
// approximation, not a real backend progress signal.
function progressPercent(run) {
  if (run.status === "completed") return 100;
  const index = activeStepIndex(run.elapsed_seconds);
  return Math.round((index / (PIPELINE_STEP_COUNT - 1)) * 100);
}

export default function RunHistoryTable({ history, liveRun, onView }) {
  const rows = liveRun ? [liveRun, ...history] : history;

  if (rows.length === 0) {
    return (
      <Paper variant="outlined" sx={{ p: 4, textAlign: "center" }}>
        <Typography variant="body2" color="text.secondary">
          No pipeline runs yet — run one above and it will show up here.
        </Typography>
      </Paper>
    );
  }

  return (
    <TableContainer component={Paper} variant="outlined">
      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>Run ID</TableCell>
            <TableCell>Session Source</TableCell>
            <TableCell>Status</TableCell>
            <TableCell>Progress</TableCell>
            <TableCell>Time Elapsed</TableCell>
            <TableCell align="right">Actions</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((run) => {
            const style = STATUS_STYLE[run.status];
            const percent = progressPercent(run);
            return (
              <TableRow key={run.run_id} hover>
                <TableCell sx={{ fontFamily: "monospace", fontSize: 12 }}>
                  run_{run.run_id.slice(0, 6)}
                </TableCell>
                <TableCell>{SOURCE_LABEL[run.source] ?? run.source}</TableCell>
                <TableCell>
                  <Stack direction="row" spacing={0.75} sx={{ alignItems: "center" }}>
                    <Box sx={{ width: 8, height: 8, borderRadius: "50%", bgcolor: style.dot }} />
                    <Typography variant="body2" sx={{ color: style.text, fontWeight: 600 }}>
                      {style.label}
                    </Typography>
                  </Stack>
                </TableCell>
                <TableCell sx={{ width: 140 }}>
                  <Stack direction="row" spacing={1} sx={{ alignItems: "center" }}>
                    <LinearProgress
                      variant="determinate"
                      value={percent}
                      color={run.status === "failed" ? "error" : run.status === "completed" ? "success" : "info"}
                      sx={{ flexGrow: 1, height: 6, borderRadius: 3 }}
                    />
                    <Typography variant="caption" color="text.secondary">
                      {percent}%
                    </Typography>
                  </Stack>
                </TableCell>
                <TableCell>{run.elapsed_seconds}s</TableCell>
                <TableCell align="right">
                  {run.status === "completed" && run.response && (
                    <Button size="small" onClick={() => onView(run)}>
                      View
                    </Button>
                  )}
                </TableCell>
              </TableRow>
            );
          })}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
