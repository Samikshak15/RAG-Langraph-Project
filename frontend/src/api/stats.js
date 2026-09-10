import { apiFetch } from "./client";

/**
 * @returns {Promise<import("../types/api").StatsResponse>}
 */
export function getStats() {
  return apiFetch("/stats");
}
