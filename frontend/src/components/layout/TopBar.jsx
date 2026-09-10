import AddIcon from "@mui/icons-material/Add";
import HelpOutlineIcon from "@mui/icons-material/HelpOutlineOutlined";
import NotificationsNoneIcon from "@mui/icons-material/NotificationsNone";
import SearchIcon from "@mui/icons-material/Search";
import Avatar from "@mui/material/Avatar";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import IconButton from "@mui/material/IconButton";
import InputAdornment from "@mui/material/InputAdornment";
import Stack from "@mui/material/Stack";
import TextField from "@mui/material/TextField";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function TopBar() {
  const navigate = useNavigate();
  const [quickQuery, setQuickQuery] = useState("");

  function submitQuickSearch() {
    if (!quickQuery.trim()) return;
    navigate(`/search?q=${encodeURIComponent(quickQuery.trim())}`);
  }

  return (
    <Box
      sx={{
        display: "flex",
        alignItems: "center",
        gap: 2,
        px: 3,
        py: 2,
        borderBottom: "1px solid",
        borderColor: "divider",
        bgcolor: "background.paper",
      }}
    >
      <TextField
        size="small"
        placeholder="Search sessions, transcripts…"
        value={quickQuery}
        onChange={(e) => setQuickQuery(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && submitQuickSearch()}
        sx={{ flexGrow: 1, maxWidth: 420 }}
        slotProps={{
          input: {
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon fontSize="small" color="disabled" />
              </InputAdornment>
            ),
          },
        }}
      />

      <Box sx={{ flexGrow: 1 }} />

      <Stack direction="row" spacing={0.5} sx={{ alignItems: "center" }}>
        <IconButton size="small" aria-label="notifications" disabled>
          <NotificationsNoneIcon fontSize="small" />
        </IconButton>
        <IconButton size="small" aria-label="help" disabled>
          <HelpOutlineIcon fontSize="small" />
        </IconButton>

        <Button variant="contained" startIcon={<AddIcon />} onClick={() => navigate("/")} sx={{ ml: 1 }}>
          New Session
        </Button>

        <Avatar sx={{ width: 32, height: 32, ml: 1, fontSize: 14, bgcolor: "secondary.main" }}>S</Avatar>
      </Stack>
    </Box>
  );
}
