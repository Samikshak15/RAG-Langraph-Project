import { useEffect, useRef, useState } from "react";
import { runPipeline } from "../api/pipeline";
import { appendRun } from "../utils/runHistory";

export function usePipelineRun() {
  const [status, setStatus] = useState("idle"); // idle | loading | success | error
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [elapsedSeconds, setElapsedSeconds] = useState(0);
  const intervalRef = useRef(null);
  const elapsedRef = useRef(0);
  const sourceRef = useRef("local");

  useEffect(() => {
    return () => clearInterval(intervalRef.current);
  }, []);

  async function run(source) {
    setStatus("loading");
    setError(null);
    setElapsedSeconds(0);
    elapsedRef.current = 0;
    sourceRef.current = source;

    intervalRef.current = setInterval(() => {
      elapsedRef.current += 1;
      setElapsedSeconds(elapsedRef.current);
    }, 1000);

    try {
      const result = await runPipeline(source);
      setData(result);
      setStatus("success");
      appendRun({
        run_id: result.session_id,
        status: "completed",
        source,
        timestamp: new Date().toISOString(),
        elapsed_seconds: elapsedRef.current,
        response: result,
      });
    } catch (err) {
      setError(err);
      setStatus("error");
      appendRun({
        run_id: `run-${new Date().toISOString()}`,
        status: "failed",
        source,
        timestamp: new Date().toISOString(),
        elapsed_seconds: elapsedRef.current,
        error_message: err?.message ?? "Unknown error",
      });
    } finally {
      clearInterval(intervalRef.current);
    }
  }

  return { status, data, error, elapsedSeconds, run };
}
