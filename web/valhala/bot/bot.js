const redis = require("redis");
const r = redis.createClient({
  port: 6379,
  host: "redis",
});

const puppeteer = require("puppeteer");
require("dotenv").config();

async function browse(url) {
  console.log(`Browsing -> ${url}`);

  const browser = await puppeteer.launch({
    args: ["--no-sandbox", "--disable-gpu"],
  });

  const page = await browser.newPage();
  await page.setCookie({
    name: "flag",
    value: "inghack{fake_flag_for_testing}",
    domain: "localhost",
    secure: false,
    samesite: "Strict"
  });

  try {
    await page.goto(url, {
      waitUntil: "networkidle2",
    });
  } catch (err) {
    console.log(err);
  }

  await page.close();
  await browser.close();

  console.log(`Done visiting -> ${url}`);
}

function main() {
  r.blpop(["submissions", 0], async (_, submit_url) => {
    let url = submit_url[1];
    await browse(url);
    main();
  });
}

console.log("XSS Bot ready");
main();
