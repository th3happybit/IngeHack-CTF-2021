const redis = require("redis");
const r = redis.createClient({
  port: 6379,
  host: "redis",
});

const puppeteer = require("puppeteer");
require('dotenv').config()

const cookie = process.env.CHALLENGE_COOKIE;
const host = process.env.CHALLENGE_HOST;
console.log(`CHALLENGE COOKIE -> ${cookie}`);
console.log(`CHALLENGE HOST -> ${host}`);
async function browse(url) {
  console.log(`Browsing -> ${url}`);
  const browser = await (
    await puppeteer.launch({
      headless: true,
      args: ["--no-sandbox", "--disable-gpu"],
    })
  ).createIncognitoBrowserContext();

  const page = await browser.newPage();
  await page.setCookie({
    name: "flag",
    value: cookie,
    domain: host,
    sameSite: "None",
    secure: true,
  });

  try {
    const resp = await page.goto(url, {
      waitUntil: "load",
      timeout: 20 * 1000,
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
