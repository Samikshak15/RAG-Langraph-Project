import Button from "@mui/material/Button";
import FormControlLabel from "@mui/material/FormControlLabel";
import Paper from "@mui/material/Paper";
import Stack from "@mui/material/Stack";
import Switch from "@mui/material/Switch";
import TextField from "@mui/material/TextField";
import SearchIcon from "@mui/icons-material/Search";

export default function SearchBar({ query, onQueryChange, onlyScored, onOnlyScoredChange, disabled, onSearch }) {
  return (
    <Paper variant="outlined" sx={{ p: 3, mb: 2 }}>
      <Stack spacing={2}>
        <Stack direction={{ xs: "column", sm: "row" }} spacing={1.5}>
          <TextField
            fullWidth
            label="Ask something about the interview"
            placeholder="e.g. how do you evaluate RAG retrieval quality"
            value={query}
            onChange={(e) => onQueryChange(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && onSearch()}
            disabled={disabled}
          />
          <Button
            variant="contained"
            startIcon={<SearchIcon />}
            onClick={onSearch}
            disabled={disabled}
            sx={{ px: 3, whiteSpace: "nowrap" }}
          >
            Search Vectors
          </Button>
        </Stack>
        <FormControlLabel
          control={
            <Switch
              checked={onlyScored}
              onChange={(e) => onOnlyScoredChange(e.target.checked)}
              disabled={disabled}
            />
          }
          label="Only curriculum-covered questions"
        />
      </Stack>
    </Paper>
  );
}
