import { useState } from "react";
import { runSearch } from "../api/search";

export function useSearch() {
  const [status, setStatus] = useState("idle"); // idle | loading | success | error
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  async function search(query, onlyScored, nResults) {
    if (!query.trim()) return;
    setStatus("loading");
    setError(null);
    try {
      const result = await runSearch(query, onlyScored, nResults);
      setData(result);
      setStatus("success");
    } catch (err) {
      setError(err);
      setStatus("error");
    }
  }

  return { status, data, error, search };
}
