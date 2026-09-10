import { apiFetch } from "./client";

/**
 * @param {number} limit
 * @param {number} offset
 * @returns {Promise<import("../types/api").ChunkListResponse>}
 */
export function listChunks(limit, offset) {
  return apiFetch(`/chunks?limit=${limit}&offset=${offset}`);
}
