import useSWR from "swr";
import { Paper, Typography } from "@material-ui/core";
import { withStyles } from "@material-ui/core/styles";

const fetcher = (query) =>
  fetch("/api/96b97cfae94f1e5deeb3f086aa34f45e/graphql", {
    method: "POST",
    headers: {
      "Content-type": "application/json",
    },
    body: JSON.stringify({ query }),
  })
    .then((res) => res.json())
    .then((json) => json.data);

const WhiteTextTypography = withStyles({
  root: {
    color: "#FFFFFF",
  },
})(Typography);

const Container = (props) => {
  return (
    <div style={{ height: "89vh", width: "514px", margin: "16px" }}>
      <Paper
        style={{ height: "100%", width: "514px", backgroundColor: props.color }}
      >
        <WhiteTextTypography align="center" variant="h6">
          {props.name}
        </WhiteTextTypography>
      </Paper>
    </div>
  );
};

export default function Index() {
  const { data, error } = useSWR("{ colors { name, hex } }", fetcher);

  if (error) return <div>Failed to load</div>;
  if (!data) return <div>Loading...</div>;

  const { colors } = data;

  return (
    <>
      <Typography align="center" variant="h3">
        Ugly Colors Palette
      </Typography>
      <div
        style={{
          width: "100%",
          overflow: "auto",
          display: "flex",
          borderRadius: 25,
        }}
      >
        {colors.map((color, i) => (
          <Container key={i} name={color.name} color={color.hex} />
        ))}
      </div>
    </>
  );
}
