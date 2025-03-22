
console.log("Loading JSON...");
const fs = require('fs');
const fileName = "../mit.json";
const fileData = fs.readFileSync(fileName, "utf8");

const on_finish = (result) => {
	console.log('Completed.');
	process.exit(0);
}

const on_progress = (percent) => {
	// console.log(percent + '%...');
}

console.log("Compressing...");
var my_lzma = require("lzma");
my_lzma.compress(fileData, on_finish, on_progress);

