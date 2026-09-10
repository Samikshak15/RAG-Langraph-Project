import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import Typography from "@mui/material/Typography";

export default function BulletList({ title, items, icon, color }) {
  return (
    <>
      <Typography variant="subtitle2" fontWeight={600} color={color}>
        {title}
      </Typography>
      {items.length === 0 ? (
        <Typography variant="body2" color="text.secondary" sx={{ pl: 1 }}>
          None
        </Typography>
      ) : (
        <List dense disablePadding>
          {items.map((item, i) => (
            <ListItem key={i} disableGutters sx={{ py: 0.25, alignItems: "flex-start" }}>
              <ListItemIcon sx={{ minWidth: 28, mt: 0.5, color }}>{icon}</ListItemIcon>
              <ListItemText primary={item} slotProps={{ primary: { variant: "body2" } }} />
            </ListItem>
          ))}
        </List>
      )}
    </>
  );
}
