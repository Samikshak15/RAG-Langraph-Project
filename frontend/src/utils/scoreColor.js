/**
 * Maps a question's score to an MUI Chip/Alert color.
 * @param {number} score
 * @param {boolean} countsTowardScore
 * @returns {"default" | "error" | "warning" | "success"}
 */
export function scoreColor(score, countsTowardScore) {
  if (!countsTowardScore) return "default";
  if (score >= 8) return "success";
  if (score >= 5) return "warning";
  return "error";
}
