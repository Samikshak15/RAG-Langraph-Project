import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Grid from "@mui/material/Grid";
import Typography from "@mui/material/Typography";

function StatCard({ label, value, color }) {
  return (
    <Grid size={{ xs: 6, sm: 4, md: 2.4 }}>
      <Card variant="outlined" sx={{ height: "100%" }}>
        <CardContent>
          <Typography variant="caption" color="text.secondary">
            {label}
          </Typography>
          <Typography variant="h4" fontWeight={700} color={color ?? "text.primary"}>
            {value}
          </Typography>
        </CardContent>
      </Card>
    </Grid>
  );
}

export default function SummaryStats({ summary }) {
  return (
    <Grid container spacing={2} sx={{ mb: 3 }}>
      <StatCard label="Total questions" value={summary.total_questions} />
      <StatCard label="Curriculum-covered" value={summary.scored_questions} color="success.main" />
      <StatCard label="Off-curriculum" value={summary.not_covered_questions} color="text.secondary" />
      <StatCard label="Average score" value={`${summary.average_score} / 10`} color="primary.main" />
      <StatCard label="Topics covered" value={summary.topics_covered.length} />
    </Grid>
  );
}
