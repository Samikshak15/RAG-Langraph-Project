import { apiFetch } from "./client";

/**
 * @param {string} query
 * @param {boolean} onlyScored
 * @param {number} [nResults]
 * @returns {Promise<import("../types/api").SearchResponse>}
 */
export function runSearch(query, onlyScored, nResults = 5) {
  return apiFetch("/search", {
    method: "POST",
    body: JSON.stringify({ query, only_scored: onlyScored, n_results: nResults }),
  });
}
