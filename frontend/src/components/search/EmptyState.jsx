import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import SearchOffIcon from "@mui/icons-material/SearchOff";
import TravelExploreIcon from "@mui/icons-material/TravelExplore";

export default function EmptyState({ hasSearched }) {
  const Icon = hasSearched ? SearchOffIcon : TravelExploreIcon;
  return (
    <Box sx={{ textAlign: "center", py: 8, color: "text.secondary" }}>
      <Icon sx={{ fontSize: 56, mb: 1, opacity: 0.5 }} />
      <Typography variant="body1">
        {hasSearched
          ? "No results found for that query."
          : "Run the pipeline on the Dashboard first, then search the stored interview content here."}
      </Typography>
    </Box>
  );
}
