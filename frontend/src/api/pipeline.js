import { apiFetch } from "./client";

/**
 * @param {import("../types/api").PipelineSource} source
 * @returns {Promise<import("../types/api").PipelineRunResponse>}
 */
export function runPipeline(source) {
  return apiFetch("/pipeline/run", {
    method: "POST",
    body: JSON.stringify({ source }),
  });
}
