import AutorenewIcon from "@mui/icons-material/Autorenew";
import ListAltIcon from "@mui/icons-material/ListAlt";
import StorageIcon from "@mui/icons-material/Storage";
import TrendingUpIcon from "@mui/icons-material/TrendingUp";
import Box from "@mui/material/Box";
import Grid from "@mui/material/Grid";
import Skeleton from "@mui/material/Skeleton";
import StatCard from "../shared/StatCard";
import { formatBytes } from "../../utils/formatBytes";

function CardIcon({ children }) {
  return (
    <Box
      sx={{
        width: 30,
        height: 30,
        borderRadius: "50%",
        bgcolor: "#efe9fc",
        color: "primary.main",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      {children}
    </Box>
  );
}

// Store-wide totals (across everything ever embedded), fetched from
// GET /api/v1/stats. Deliberately separate from SummaryStats.jsx, which
// shows only the current run's results — conflating the two would be
// confusing ("is this number about this run, or everything?").
//
// Total Chunks and Total Embeddings intentionally show the same number:
// this pipeline creates exactly one embedding per chunk, so they are
// genuinely equal, not a display bug. No fabricated week-over-week deltas
// are shown (e.g. "+12% this week") since there's no historical time
// series to compute that from honestly.
export default function OverviewStats({ stats, loading }) {
  if (loading || !stats) {
    return (
      <Grid container spacing={2} sx={{ mb: 3 }}>
        {[0, 1, 2, 3].map((i) => (
          <Grid size={{ xs: 12, sm: 6, md: 3 }} key={i}>
            <Skeleton variant="rounded" height={104} />
          </Grid>
        ))}
      </Grid>
    );
  }

  return (
    <Grid container spacing={2} sx={{ mb: 3 }}>
      <Grid size={{ xs: 12, sm: 6, md: 3 }}>
        <StatCard
          label="Total Sessions"
          value={stats.distinct_sessions.toLocaleString()}
          sublabel="Distinct sessions embedded"
          decoration={
            <CardIcon>
              <AutorenewIcon fontSize="small" />
            </CardIcon>
          }
        />
      </Grid>
      <Grid size={{ xs: 12, sm: 6, md: 3 }}>
        <StatCard
          label="Total Chunks"
          value={stats.total_chunks.toLocaleString()}
          sublabel="Stored in ChromaDB"
          decoration={
            <CardIcon>
              <ListAltIcon fontSize="small" />
            </CardIcon>
          }
        />
      </Grid>
      <Grid size={{ xs: 12, sm: 6, md: 3 }}>
        <StatCard
          label="Total Embeddings"
          value={stats.total_chunks.toLocaleString()}
          sublabel="1 embedding per chunk"
          decoration={
            <CardIcon>
              <TrendingUpIcon fontSize="small" />
            </CardIcon>
          }
        />
      </Grid>
      <Grid size={{ xs: 12, sm: 6, md: 3 }}>
        <StatCard
          label="Vector Store Size"
          value={formatBytes(stats.vector_store_bytes)}
          sublabel="ChromaDB on-disk data"
          decoration={
            <CardIcon>
              <StorageIcon fontSize="small" />
            </CardIcon>
          }
        />
      </Grid>
    </Grid>
  );
}
