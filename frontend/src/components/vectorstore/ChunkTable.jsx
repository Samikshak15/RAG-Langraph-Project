import Chip from "@mui/material/Chip";
import Paper from "@mui/material/Paper";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TablePagination from "@mui/material/TablePagination";
import TableRow from "@mui/material/TableRow";
import Typography from "@mui/material/Typography";
import { formatRelativeTime } from "../../utils/formatRelativeTime";
import { scoreColor } from "../../utils/scoreColor";

export default function ChunkTable({ chunks, total, page, setPage, pageSize, loading }) {
  if (!loading && chunks.length === 0) {
    return (
      <Paper variant="outlined" sx={{ p: 4, textAlign: "center" }}>
        <Typography variant="body2" color="text.secondary">
          No chunks stored yet — run the pipeline on the Dashboard first.
        </Typography>
      </Paper>
    );
  }

  return (
    <Paper variant="outlined">
      <TableContainer>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>Chunk ID</TableCell>
              <TableCell>Question ID</TableCell>
              <TableCell>Topic / Subtopic</TableCell>
              <TableCell>Score</TableCell>
              <TableCell>Counts Toward Score</TableCell>
              <TableCell>Stored At</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {chunks.map((chunk) => (
              <TableRow key={chunk.chunk_id} hover>
                <TableCell sx={{ fontFamily: "monospace", fontSize: 12 }}>{chunk.chunk_id}</TableCell>
                <TableCell>{chunk.question_id}</TableCell>
                <TableCell>
                  <Typography variant="body2">{chunk.topic}</Typography>
                  <Typography variant="caption" color="text.secondary">
                    {chunk.subtopic}
                  </Typography>
                </TableCell>
                <TableCell>
                  <Chip
                    size="small"
                    label={`${chunk.score}/10`}
                    color={scoreColor(chunk.score, chunk.counts_toward_score)}
                  />
                </TableCell>
                <TableCell>
                  <Chip
                    size="small"
                    variant="outlined"
                    label={chunk.counts_toward_score ? "Yes" : "No"}
                  />
                </TableCell>
                <TableCell>{formatRelativeTime(chunk.stored_at)}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      <TablePagination
        component="div"
        count={total}
        page={page}
        onPageChange={(_, newPage) => setPage(newPage)}
        rowsPerPage={pageSize}
        rowsPerPageOptions={[pageSize]}
      />
    </Paper>
  );
}
