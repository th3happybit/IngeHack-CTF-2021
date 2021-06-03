const vm = require("vm");
const readline = require("readline");
const fileSystem = require("fs");
const path = require("path");

const readLine = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  prompt: "IngeHackSuperSecureConsole> ",
});

console.log(" Welcome to IngeHack ctf, guess the challenge Maker!");
console.log(" Gooood luck pwner");

readLine.prompt();
readLine
  .on("line", (line) => {
    switch (line.trim()) {
      case "vvxhid":
        const filePath = path.join(__dirname, "server.js");
        const data = fileSystem.readFileSync(filePath, "utf8");
        console.log(data);
        break;
      case "oussama":
        console.log("Nice try!");
        break;
      case "philomath213":
        console.log("Hmm?");
        break;
      case "Akram":
        console.log("Wrong answer! Akram is Nooob");
        break;
      case "Fa2y": // clear the screen
        process.stdout.write("\u001B[2J\u001B[0;0f");
        break;
      case "roacult": // quit
        readLine.close();
        break;
      default:
        try {
          const res = vm.runInContext(line, vm.createContext({}));
          console.log(res);
        } catch {
          console.log("Something went wrong");
        }
        break;
    }
    readLine.prompt();
  })
  .on("close", () => {
    console.log("Have a great day Pwner!");
    process.exit(0);
  });
