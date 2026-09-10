import { createTheme } from "@mui/material/styles";

const theme = createTheme({
  palette: {
    mode: "light",
    primary: { main: "#7c3aed" },
    secondary: { main: "#0ea5e9" },
    background: { default: "#13111c", paper: "#ffffff" },
  },
  shape: { borderRadius: 10 },
  typography: {
    fontFamily: [
      "Inter",
      "-apple-system",
      "BlinkMacSystemFont",
      "Segoe UI",
      "Roboto",
      "sans-serif",
    ].join(","),
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: { boxShadow: "0 1px 3px rgba(15, 23, 42, 0.08)" },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: { textTransform: "none", fontWeight: 600 },
      },
    },
  },
});

// Sidebar-specific palette — kept separate from the MUI theme's light content
// palette since the sidebar is deliberately dark while page content stays light.
export const sidebar = {
  background: "#1a1625",
  backgroundHover: "#241f33",
  border: "#2d2740",
  text: "#c7c2d6",
  textActive: "#ffffff",
};

export default theme;
