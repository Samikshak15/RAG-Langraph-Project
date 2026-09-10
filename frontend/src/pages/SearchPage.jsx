import CircularProgress from "@mui/material/CircularProgress";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import ErrorBanner from "../components/dashboard/ErrorBanner";
import EmptyState from "../components/search/EmptyState";
import ResultCard from "../components/search/ResultCard";
import SearchBar from "../components/search/SearchBar";
import SuggestedChips from "../components/search/SuggestedChips";
import { useSearch } from "../hooks/useSearch";

const N_RESULTS = 5;

export default function SearchPage() {
  const [searchParams] = useSearchParams();
  const [query, setQuery] = useState(searchParams.get("q") ?? "");
  const [onlyScored, setOnlyScored] = useState(false);
  const { status, data, error, search } = useSearch();
  const loading = status === "loading";
  const hasSearched = status !== "idle";

  function runSearch(q = query) {
    search(q, onlyScored, N_RESULTS);
  }

  // Auto-run once if we arrived here with ?q= from the top-bar quick search.
  useEffect(() => {
    const initial = searchParams.get("q");
    if (initial) runSearch(initial);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <>
      <Typography variant="h5" fontWeight={700} gutterBottom>
        Semantic Similarity Search
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Query your vector database using natural language to find the most relevant interview
        segments, transcript chunks, and context.
      </Typography>

      <SearchBar
        query={query}
        onQueryChange={setQuery}
        onlyScored={onlyScored}
        onOnlyScoredChange={setOnlyScored}
        disabled={loading}
        onSearch={() => runSearch()}
      />

      <SuggestedChips
        onPick={(text) => {
          setQuery(text);
          search(text, onlyScored, N_RESULTS);
        }}
      />

      {loading && (
        <Stack sx={{ alignItems: "center", py: 6 }}>
          <CircularProgress />
        </Stack>
      )}

      {status === "error" && <ErrorBanner error={error} />}

      {status === "success" && data && data.results.length > 0 && (
        <>
          <Typography variant="subtitle2" color="text.secondary" sx={{ mb: 1.5 }}>
            Top {data.results.length} Results — "{data.query}"
          </Typography>
          <Stack>
            {data.results.map((result) => (
              <ResultCard key={result.chunk_id} result={result} />
            ))}
          </Stack>
        </>
      )}

      {status === "success" && data && data.results.length === 0 && <EmptyState hasSearched />}
      {status === "idle" && <EmptyState hasSearched={false} />}
    </>
  );
}
