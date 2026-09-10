import { apiFetch } from "./client";

export async function getCandidates(limit = 2000, search = null, auto_discover = false) {
  let url = `/candidates?limit=${limit}&auto_discover=${auto_discover}`;
  if (search) {
    url += `&search=${encodeURIComponent(search)}`;
  }
  return apiFetch(url);
}

export async function getCandidateHistory(query, limit = 3) {
  return apiFetch(`/candidate/${encodeURIComponent(query)}/history?limit=${limit}`);
}

export async function ingestCandidateTranscripts(query, limit = 3) {
  return apiFetch(`/candidate/${encodeURIComponent(query)}/ingest?limit=${limit}`, {
    method: "POST",
  });
}

export async function queryCandidateRAG(candidate, query, n_results = 5, only_scored = false) {
  return apiFetch("/candidate/query", {
    method: "POST",
    body: JSON.stringify({
      candidate,
      query,
      n_results,
      only_scored,
    }),
  });
}

export async function analyzeCandidate(candidate, query = "What are the candidate's main weaknesses across recent interviews?", num_interviews = 3) {
  return apiFetch("/candidate/analyze", {
    method: "POST",
    body: JSON.stringify({
      candidate,
      query,
      num_interviews,
    }),
  });
}
