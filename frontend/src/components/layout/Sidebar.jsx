import Box from "@mui/material/Box";
import Drawer from "@mui/material/Drawer";
import List from "@mui/material/List";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import Typography from "@mui/material/Typography";
import BadgeOutlinedIcon from "@mui/icons-material/BadgeOutlined";
import DashboardOutlinedIcon from "@mui/icons-material/DashboardOutlined";
import PsychologyAltIcon from "@mui/icons-material/PsychologyAlt";
import SearchOutlinedIcon from "@mui/icons-material/SearchOutlined";
import StorageOutlinedIcon from "@mui/icons-material/StorageOutlined";
import { NavLink } from "react-router-dom";
import { sidebar } from "../../theme";

const WIDTH = 240;

const NAV_ITEMS = [
  { label: "Candidate Hub", to: "/candidates", icon: <BadgeOutlinedIcon /> },
  { label: "Dashboard", to: "/", icon: <DashboardOutlinedIcon /> },
  { label: "Search", to: "/search", icon: <SearchOutlinedIcon /> },
  { label: "Vector Store", to: "/vector-store", icon: <StorageOutlinedIcon /> },
];

export default function Sidebar() {
  return (
    <Drawer
      variant="permanent"
      sx={{
        width: WIDTH,
        flexShrink: 0,
        [`& .MuiDrawer-paper`]: {
          width: WIDTH,
          boxSizing: "border-box",
          bgcolor: sidebar.background,
          borderRight: `1px solid ${sidebar.border}`,
          color: sidebar.text,
        },
      }}
    >
      <Box sx={{ display: "flex", alignItems: "center", gap: 1.5, px: 2.5, py: 2.5 }}>
        <Box
          sx={{
            width: 34,
            height: 34,
            borderRadius: 1.5,
            bgcolor: "primary.main",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <PsychologyAltIcon sx={{ fontSize: 20, color: "#fff" }} />
        </Box>
        <Box>
          
          <Typography variant="caption" color={sidebar.text}>
            Interview Intelligence
          </Typography>
        </Box>
      </Box>

      <List sx={{ px: 1.5 }}>
        {NAV_ITEMS.map((item) => (
          <ListItemButton
            key={item.to}
            component={NavLink}
            to={item.to}
            end={item.to === "/"}
            sx={{
              borderRadius: 2,
              mb: 0.5,
              color: sidebar.text,
              "&:hover": { bgcolor: sidebar.backgroundHover },
              "&.active": {
                bgcolor: "primary.main",
                color: sidebar.textActive,
                "& .MuiListItemIcon-root": { color: sidebar.textActive },
              },
            }}
          >
            <ListItemIcon sx={{ minWidth: 36, color: "inherit" }}>{item.icon}</ListItemIcon>
            <ListItemText primary={item.label} slotProps={{ primary: { fontWeight: 600, fontSize: 14 } }} />
          </ListItemButton>
        ))}
      </List>
    </Drawer>
  );
}
