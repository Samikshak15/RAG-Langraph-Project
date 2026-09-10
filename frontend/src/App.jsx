import { Route, Routes } from "react-router-dom";
import AppShell from "./components/layout/AppShell";
import CandidateHubPage from "./pages/CandidateHubPage";
import DashboardPage from "./pages/DashboardPage";
import SearchPage from "./pages/SearchPage";
import VectorStorePage from "./pages/VectorStorePage";

export default function App() {
  return (
    <Routes>
      <Route element={<AppShell />}>
        <Route path="/" element={<CandidateHubPage />} />
        <Route path="/candidates" element={<CandidateHubPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/search" element={<SearchPage />} />
        <Route path="/vector-store" element={<VectorStorePage />} />
      </Route>
    </Routes>
  );
}
