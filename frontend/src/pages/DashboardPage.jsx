import Button from "@mui/material/Button";
import CalendarTodayOutlinedIcon from "@mui/icons-material/CalendarTodayOutlined";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
import { useEffect, useState } from "react";
import ErrorBanner from "../components/dashboard/ErrorBanner";
import OverviewStats from "../components/dashboard/OverviewStats";
import PipelineStepper from "../components/dashboard/PipelineStepper";
import QuestionAccordion from "../components/dashboard/QuestionAccordion";
import RunHistoryTable from "../components/dashboard/RunHistoryTable";
import SourcePicker from "../components/dashboard/SourcePicker";
import SummaryStats from "../components/dashboard/SummaryStats";
import { usePipelineRun } from "../hooks/usePipelineRun";
import { useStats } from "../hooks/useStats";
import { getRunHistory } from "../utils/runHistory";

export default function DashboardPage() {
  const { status, data, error, elapsedSeconds, run } = usePipelineRun();
  const { stats, loading: statsLoading, refetch: refetchStats } = useStats();
  const [history, setHistory] = useState(() => getRunHistory());
  const [viewedRun, setViewedRun] = useState(null);

  const loading = status === "loading";

  // Refresh both the store-wide stats and the run-history table once a run
  // finishes (success or failure) — the history entry was just written by
  // usePipelineRun, and total_chunks/sessions may have changed on success.
  useEffect(() => {
    if (status === "success" || status === "error") {
      setHistory(getRunHistory());
      if (status === "success") refetchStats();
    }
  }, [status, refetchStats]);

  const displayedResult = viewedRun ? viewedRun.response : status === "success" ? data : null;

  const liveRun = loading
    ? { run_id: "current", status: "loading", source: "local", elapsed_seconds: elapsedSeconds }
    : null;

  function handleRun(source) {
    setViewedRun(null);
    run(source);
  }

  return (
    <>
      <Stack
        direction={{ xs: "column", sm: "row" }}
        sx={{ justifyContent: "space-between", alignItems: { sm: "center" }, mb: 3 }}
      >
        <Stack>
          <Typography variant="h5" fontWeight={700}>
            Welcome — Admin
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Here is the current state of your Interview Intelligence RAG system.
          </Typography>
        </Stack>
        <Button variant="outlined" size="small" startIcon={<CalendarTodayOutlinedIcon fontSize="small" />}>
          Last 30 Days
        </Button>
      </Stack>

      <OverviewStats stats={stats} loading={statsLoading} />

      <PipelineStepper status={loading ? "loading" : status} elapsedSeconds={elapsedSeconds} />

      <SourcePicker disabled={loading} onRun={handleRun} />

      {status === "error" && !loading && (
        <ErrorBanner error={error} onRetry={() => run("local")} />
      )}

      {displayedResult && (
        <>
          <Typography variant="subtitle1" fontWeight={600} sx={{ mb: 1.5 }}>
            {viewedRun ? `Viewing run_${viewedRun.run_id.slice(0, 6)}` : "This run's results"}
          </Typography>
          <SummaryStats summary={displayedResult.summary} />
          <Typography variant="subtitle1" fontWeight={600} sx={{ mb: 1.5 }}>
            Per-question breakdown
          </Typography>
          <Stack sx={{ mb: 3 }}>
            {displayedResult.results.map((record) => (
              <QuestionAccordion key={record.question_id} record={record} />
            ))}
          </Stack>
        </>
      )}

      <Typography variant="subtitle1" fontWeight={600} sx={{ mb: 1.5 }}>
        Recent Pipeline Runs
      </Typography>
      <RunHistoryTable history={history} liveRun={liveRun} onView={setViewedRun} />
    </>
  );
}
