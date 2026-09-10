import Box from "@mui/material/Box";
import { Outlet } from "react-router-dom";
import Sidebar from "./Sidebar";
import TopBar from "./TopBar";

export default function AppShell() {
  return (
    <Box sx={{ display: "flex", minHeight: "100vh" }}>
      <Sidebar />
      <Box sx={{ flexGrow: 1, display: "flex", flexDirection: "column", minWidth: 0 }}>
        <TopBar />
        <Box sx={{ flexGrow: 1, bgcolor: "#f4f2fa", p: 3 }}>
          <Outlet />
        </Box>
      </Box>
    </Box>
  );
}
