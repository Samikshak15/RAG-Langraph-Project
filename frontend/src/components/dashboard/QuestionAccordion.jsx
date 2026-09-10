import Accordion from "@mui/material/Accordion";
import AccordionDetails from "@mui/material/AccordionDetails";
import AccordionSummary from "@mui/material/AccordionSummary";
import Alert from "@mui/material/Alert";
import Chip from "@mui/material/Chip";
import Grid from "@mui/material/Grid";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
import CheckCircleOutlineIcon from "@mui/icons-material/CheckCircleOutlined";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import FlagOutlinedIcon from "@mui/icons-material/FlagOutlined";
import HighlightOffIcon from "@mui/icons-material/HighlightOff";
import BulletList from "../shared/BulletList";
import { scoreColor } from "../../utils/scoreColor";

export default function QuestionAccordion({ record }) {
  const color = scoreColor(record.score, record.counts_toward_score);

  return (
    <Accordion variant="outlined" disableGutters sx={{ mb: 1 }}>
      <AccordionSummary expandIcon={<ExpandMoreIcon />}>
        <Stack direction="row" spacing={1.5} useFlexGap sx={{ alignItems: "center", flexWrap: "wrap", width: "100%" }}>
          <Chip label={`${record.score}/10`} color={color} size="small" sx={{ fontWeight: 700 }} />
          <Typography sx={{ flexGrow: 1, minWidth: 0, fontWeight: 500 }} noWrap>
            {record.question_id} — {record.question}
          </Typography>
          <Chip label={record.topic} size="small" variant="outlined" />
          <Chip label={record.subtopic} size="small" variant="outlined" />
          {!record.counts_toward_score && (
            <Chip label="off-curriculum" size="small" color="default" variant="outlined" />
          )}
        </Stack>
      </AccordionSummary>

      <AccordionDetails>
        <Typography variant="body2" sx={{ mb: 1 }}>
          <strong>Question:</strong> {record.question}
        </Typography>
        <Typography variant="body2" sx={{ mb: 2 }}>
          <strong>Answer:</strong> {record.answer}
        </Typography>

        <Grid container spacing={2} sx={{ mb: 2 }}>
          <Grid size={{ xs: 12, sm: 4 }}>
            <BulletList
              title="Strengths"
              items={record.strengths}
              icon={<CheckCircleOutlineIcon fontSize="small" />}
              color="success.main"
            />
          </Grid>
          <Grid size={{ xs: 12, sm: 4 }}>
            <BulletList
              title="Weaknesses"
              items={record.weaknesses}
              icon={<HighlightOffIcon fontSize="small" />}
              color="error.main"
            />
          </Grid>
          <Grid size={{ xs: 12, sm: 4 }}>
            <BulletList
              title="Missing concepts"
              items={record.missing_concepts}
              icon={<FlagOutlinedIcon fontSize="small" />}
              color="warning.main"
            />
          </Grid>
        </Grid>

        <Alert severity="info" variant="outlined">
          {record.feedback}
        </Alert>
      </AccordionDetails>
    </Accordion>
  );
}
