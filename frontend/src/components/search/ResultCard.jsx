import Box from "@mui/material/Box";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Chip from "@mui/material/Chip";
import Collapse from "@mui/material/Collapse";
import Grid from "@mui/material/Grid";
import Link from "@mui/material/Link";
import Stack from "@mui/material/Stack";
import Tooltip from "@mui/material/Tooltip";
import Typography from "@mui/material/Typography";
import CheckCircleOutlineIcon from "@mui/icons-material/CheckCircleOutlined";
import FlagOutlinedIcon from "@mui/icons-material/FlagOutlined";
import HighlightOffIcon from "@mui/icons-material/HighlightOff";
import { useState } from "react";
import BulletList from "../shared/BulletList";
import { scoreColor } from "../../utils/scoreColor";

export default function ResultCard({ result }) {
  const [expanded, setExpanded] = useState(false);
  const color = scoreColor(result.score, result.counts_toward_score);
  const relevance = (1 - result.distance).toFixed(2);

  return (
    <Card variant="outlined" sx={{ mb: 2 }}>
      <CardContent>
        <Stack direction="row" spacing={1.5} sx={{ alignItems: "flex-start" }}>
          <Box
            sx={{
              flexShrink: 0,
              width: 40,
              height: 40,
              borderRadius: "50%",
              bgcolor: "primary.main",
              color: "#fff",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: 13,
              fontWeight: 700,
            }}
          >
            {relevance}
          </Box>

          <Box sx={{ flexGrow: 1, minWidth: 0 }}>
            <Stack direction="row" spacing={1} useFlexGap sx={{ alignItems: "center", flexWrap: "wrap", mb: 0.5 }}>
              <Chip label={result.topic} size="small" variant="outlined" />
              <Chip label={`${result.score}/10`} size="small" color={color} sx={{ fontWeight: 700 }} />
              <Tooltip title="Cross-encoder relevance score (unbounded, higher = more relevant) — not a percentage">
                <Chip label={`Rerank ${result.rerank_score.toFixed(2)}`} size="small" variant="outlined" color="default" />
              </Tooltip>
            </Stack>
            <Typography variant="subtitle2" fontWeight={600}>
              {result.question}
            </Typography>
            <Typography variant="body2" color="text.secondary" noWrap>
              {result.answer}
            </Typography>
            <Stack direction="row" sx={{ justifyContent: "space-between", alignItems: "center", mt: 1 }}>
              <Typography variant="caption" color="text.secondary">
                Candidate #{result.user_id}
              </Typography>
              <Link component="button" variant="caption" onClick={() => setExpanded((v) => !v)}>
                {expanded ? "Hide details" : "View Details →"}
              </Link>
            </Stack>
          </Box>
        </Stack>

        <Collapse in={expanded}>
          <Box sx={{ mt: 2, pt: 2, borderTop: "1px solid", borderColor: "divider" }}>
            <Typography variant="body2" sx={{ mb: 2 }}>
              <strong>Full answer:</strong> {result.answer}
            </Typography>
            <Grid container spacing={2}>
              <Grid size={{ xs: 12, sm: 4 }}>
                <BulletList
                  title="Strengths"
                  items={result.strengths}
                  icon={<CheckCircleOutlineIcon fontSize="small" />}
                  color="success.main"
                />
              </Grid>
              <Grid size={{ xs: 12, sm: 4 }}>
                <BulletList
                  title="Weaknesses"
                  items={result.weaknesses}
                  icon={<HighlightOffIcon fontSize="small" />}
                  color="error.main"
                />
              </Grid>
              <Grid size={{ xs: 12, sm: 4 }}>
                <BulletList
                  title="Missing concepts"
                  items={result.missing_concepts}
                  icon={<FlagOutlinedIcon fontSize="small" />}
                  color="warning.main"
                />
              </Grid>
            </Grid>
          </Box>
        </Collapse>
      </CardContent>
    </Card>
  );
}
