import Autocomplete from "@mui/material/Autocomplete";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Chip from "@mui/material/Chip";
import CircularProgress from "@mui/material/CircularProgress";
import Stack from "@mui/material/Stack";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import CloudDownloadOutlinedIcon from "@mui/icons-material/CloudDownloadOutlined";
import PersonOutlinedIcon from "@mui/icons-material/PersonOutlined";
import RefreshOutlinedIcon from "@mui/icons-material/RefreshOutlined";
import StorageOutlinedIcon from "@mui/icons-material/StorageOutlined";
import { useEffect, useState } from "react";
import { getCandidates } from "../../api/candidates";

export default function CandidateSelector({
  selectedCandidate,
  onSelectCandidate,
  onIngestTranscripts,
  ingestLoading,
}) {
  const [candidates, setCandidates] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchList = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await getCandidates(2000);
      const list = res.candidates || [];
      setCandidates(list);

      // Default selection to candidate 2071 or first candidate if none selected
      if (!selectedCandidate && list.length > 0) {
        const defaultCand = list.find((c) => String(c.user_id) === "2071") || list[0];
        onSelectCandidate(defaultCand);
      }
    } catch (err) {
      setError(err.message || "Failed to load candidates");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchList();
  }, []);

  return (
    <Card sx={{ mb: 3, borderRadius: 3, boxShadow: "0 4px 20px rgba(0,0,0,0.05)", border: "1px solid #eef0f4" }}>
      <CardContent sx={{ p: 3 }}>
        <Stack direction={{ xs: "column", md: "row" }} spacing={3} alignItems={{ md: "center" }} justifyContent="space-between">
          <Box sx={{ flexGrow: 1, maxWidth: { md: 550 } }}>
            <Typography variant="subtitle2" fontWeight={700} color="text.secondary" sx={{ mb: 1, textTransform: "uppercase", letterSpacing: 0.5 }}>
              Select Candidate Identity
            </Typography>
            <Autocomplete
              options={candidates}
              loading={loading}
              getOptionLabel={(option) => (option ? `${option.name} (ID: ${option.user_id})` : "")}
              isOptionEqualToValue={(opt, val) => String(opt.user_id) === String(val.user_id)}
              value={selectedCandidate}
              onChange={(_, newValue) => onSelectCandidate(newValue)}
              renderInput={(params) => (
                <TextField
                  {...params}
                  placeholder="Search candidate name or enter user_id (e.g. 2071, Sejal)..."
                  variant="outlined"
                  size="small"
                  InputProps={{
                    ...params.InputProps,
                    startAdornment: (
                      <>
                        <PersonOutlinedIcon color="action" sx={{ mr: 1, fontSize: 20 }} />
                        {params.InputProps.startAdornment}
                      </>
                    ),
                    endAdornment: (
                      <>
                        {loading ? <CircularProgress color="inherit" size={20} /> : null}
                        {params.InputProps.endAdornment}
                      </>
                    ),
                  }}
                />
              )}
              renderOption={(props, option) => {
                const { key, ...optionProps } = props;
                return (
                  <Box component="li" key={key} {...optionProps} sx={{ py: 1, px: 2 }}>
                    <Stack direction="row" alignItems="center" justifyContent="space-between" sx={{ width: "100%" }}>
                      <Box>
                        <Typography variant="body2" fontWeight={600}>
                          {option.name}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          User ID: {option.user_id} {option.email ? `• ${option.email}` : ""}
                        </Typography>
                      </Box>
                      <Chip
                        label={option.source === "mongo_db" ? "MongoDB" : "S3 Bucket"}
                        size="small"
                        color={option.source === "mongo_db" ? "primary" : "info"}
                        variant="outlined"
                        sx={{ fontSize: 10, height: 20 }}
                      />
                    </Stack>
                  </Box>
                );
              }}
            />
          </Box>

          {selectedCandidate && (
            <Stack direction="row" spacing={1.5} alignItems="center">
              <Box sx={{ p: 1.5, borderRadius: 2, bgcolor: "#f8f9fc", border: "1px solid #eef0f4", minWidth: 200 }}>
                <Typography variant="caption" color="text.secondary" fontWeight={600}>
                  Active Candidate
                </Typography>
                <Typography variant="body2" fontWeight={700} color="primary.main">
                  {selectedCandidate.name}
                </Typography>
                <Stack direction="row" spacing={1} alignItems="center" mt={0.5}>
                  <Chip
                    icon={<StorageOutlinedIcon style={{ fontSize: 12 }} />}
                    label={`ID: ${selectedCandidate.user_id}`}
                    size="small"
                    sx={{ fontSize: 11, height: 20, bgcolor: "#eee8fb", color: "#5e35b1" }}
                  />
                  <Typography variant="caption" color="text.secondary">
                    {candidates.length} candidates loaded
                  </Typography>
                </Stack>
              </Box>

              <Button
                variant="contained"
                color="primary"
                size="medium"
                disabled={ingestLoading}
                startIcon={ingestLoading ? <CircularProgress size={16} color="inherit" /> : <CloudDownloadOutlinedIcon />}
                onClick={() => onIngestTranscripts(selectedCandidate.user_id)}
                sx={{ height: 42, px: 2, textTransform: "none", fontWeight: 600 }}
              >
                {ingestLoading ? "Ingesting S3..." : "Ingest S3 Transcripts"}
              </Button>

              <Button
                variant="outlined"
                color="inherit"
                size="medium"
                onClick={fetchList}
                sx={{ height: 42, minWidth: 42, p: 0 }}
              >
                <RefreshOutlinedIcon fontSize="small" />
              </Button>
            </Stack>
          )}
        </Stack>
      </CardContent>
    </Card>
  );
}
