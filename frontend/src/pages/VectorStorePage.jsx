import Grid from "@mui/material/Grid";
import Skeleton from "@mui/material/Skeleton";
import Typography from "@mui/material/Typography";
import ChunkTable from "../components/vectorstore/ChunkTable";
import StatCard from "../components/shared/StatCard";
import { useChunks } from "../hooks/useChunks";
import { useStats } from "../hooks/useStats";
import { formatRelativeTime } from "../utils/formatRelativeTime";

export default function VectorStorePage() {
  const { stats, loading: statsLoading } = useStats();
  const { chunks, total, loading, page, setPage, pageSize } = useChunks(20);

  return (
    <>
      <Typography variant="h5" fontWeight={700} gutterBottom>
        Vector Store Exploratory View
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Browse every question-level chunk currently indexed in ChromaDB, with similarity/coverage
        metadata.
      </Typography>

      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid size={{ xs: 12, sm: 4 }}>
          {statsLoading || !stats ? (
            <Skeleton variant="rounded" height={104} />
          ) : (
            <StatCard label="Total Chunks Indexed" value={stats.total_chunks.toLocaleString()} />
          )}
        </Grid>
        <Grid size={{ xs: 12, sm: 4 }}>
          {statsLoading || !stats ? (
            <Skeleton variant="rounded" height={104} />
          ) : (
            <StatCard label="Avg Answer Score" value={`${stats.avg_score} / 10`} />
          )}
        </Grid>
        <Grid size={{ xs: 12, sm: 4 }}>
          {statsLoading || !stats ? (
            <Skeleton variant="rounded" height={104} />
          ) : (
            <StatCard label="Recent Sync" value={formatRelativeTime(stats.last_stored_at)} />
          )}
        </Grid>
      </Grid>

      <Typography variant="subtitle1" fontWeight={600} sx={{ mb: 1.5 }}>
        Question Embeddings
      </Typography>
      <ChunkTable
        chunks={chunks}
        total={total}
        page={page}
        setPage={setPage}
        pageSize={pageSize}
        loading={loading}
      />
    </>
  );
}
