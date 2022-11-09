const { renderSync } = require("sass");
const { writeFileSync } = require('fs');

const result = renderSync({
	style: "compressed",
	file: 'scss/dashboard.scss',
	loadPaths: ['node_modules'],
	includePaths: ['node_modules']
});

writeFileSync('gov_uk_dashboards/assets/dashboard.css', result.css, { encoding: 'utf8', flag: 'w' })