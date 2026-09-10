import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";

export default function StatCard({ label, value, sublabel, decoration }) {
  return (
    <Card variant="outlined" sx={{ height: "100%" }}>
      <CardContent>
        <Stack direction="row" sx={{ alignItems: "flex-start", justifyContent: "space-between" }}>
          <Stack spacing={0.5}>
            <Typography variant="caption" color="text.secondary">
              {label}
            </Typography>
            <Typography variant="h4" fontWeight={700}>
              {value}
            </Typography>
            {sublabel && (
              <Typography variant="caption" color="text.secondary">
                {sublabel}
              </Typography>
            )}
          </Stack>
          {decoration}
        </Stack>
      </CardContent>
    </Card>
  );
}
