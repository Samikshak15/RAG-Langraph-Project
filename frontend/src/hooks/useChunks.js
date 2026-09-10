import { useEffect, useState } from "react";
import { listChunks } from "../api/chunks";

export function useChunks(pageSize = 20) {
  const [page, setPage] = useState(0);
  const [chunks, setChunks] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);

    listChunks(pageSize, page * pageSize)
      .then((result) => {
        if (cancelled) return;
        setChunks(result.chunks);
        setTotal(result.total);
      })
      .catch((err) => {
        if (!cancelled) setError(err);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [page, pageSize]);

  return { chunks, total, loading, error, page, setPage, pageSize };
}
