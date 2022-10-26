const { renderSync } = require("sass");
const { writeFileSync } = require('fs');

// todo: compile should be use in future however having issue as load path not as good and not finding node_modules from MOJ
const result = renderSync({
	style: "compressed",
	file: 'scss/dashboard.scss',
	loadPaths: ['node_modules'],
	includePaths: ['node_modules']
});

writeFileSync('assets/dashboard.css', result.css, { encoding: 'utf8', flag: 'w' })