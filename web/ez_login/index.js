const express = require("express");
var cookieParser = require("cookie-parser");

const app = express();
app.use(cookieParser());

const PORT = 3000;
const AUTHORIZED_TOKENS = {};

const isAuthorized = (req, res, next) => {
  if (req.cookies) {
    const token = req.cookies.token;
    if (token && AUTHORIZED_TOKENS[token]) {
      next();
    } 
  }
  res.json({
    message: "Hello Stranger! Who are you?",
  });
};

app.get("/", isAuthorized, (req, res) => {
  res.json({
    message: "Good job! here is your flag: IngeHack{}",
  });
});

// Listen
app.listen(PORT, () => {
  console.log(`Listening on port: ${PORT}`);
});
