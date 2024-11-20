const sass = require("sass");
const { writeFileSync } = require("fs");
 
// Compile SCSS asynchronously
const result = sass.compile("scss/dashboard.scss", {
  style: "compressed",
  loadPaths: ["node_modules"], // Paths for imports
});
 
// Write the compiled CSS to a file
writeFileSync("gov_uk_dashboards/assets/dashboard.css", result.css, {
  encoding: "utf8",
  flag: "w",
});
 
console.log("SCSS compiled successfully to gov_uk_dashboards/assets/dashboard.css");