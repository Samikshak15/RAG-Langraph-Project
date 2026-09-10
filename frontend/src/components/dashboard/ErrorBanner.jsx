import Alert from "@mui/material/Alert";
import Button from "@mui/material/Button";

export default function ErrorBanner({ error, onRetry }) {
  return (
    <Alert
      severity="error"
      variant="outlined"
      sx={{ mb: 3 }}
      action={
        onRetry && (
          <Button color="inherit" size="small" onClick={onRetry}>
            Retry
          </Button>
        )
      }
    >
      {error?.message ?? "Something went wrong."}
    </Alert>
  );
}
