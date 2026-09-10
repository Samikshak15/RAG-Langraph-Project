// Per-browser pipeline run history. There is no run/session persistence on
// the backend (every /pipeline/run call is stateless), so this is the only
// honest way to show "recent runs" without fabricating server-side history —
// every entry here is a genuinely real run this browser executed.

const STORAGE_KEY = "iirag.runHistory.v1";
const MAX_ENTRIES = 20;

/**
 * @returns {Array<object>}
 */
export function getRunHistory() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

/**
 * @param {object} entry - { run_id, status, source, timestamp, elapsed_seconds, response?, error_message? }
 */
export function appendRun(entry) {
  try {
    const existing = getRunHistory();
    const next = [entry, ...existing].slice(0, MAX_ENTRIES);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
  } catch {
    // localStorage can throw under quota limits or private-mode browsing —
    // history is a convenience, not critical, so fail silently.
  }
}
