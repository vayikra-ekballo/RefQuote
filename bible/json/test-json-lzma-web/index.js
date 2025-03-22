
import { readFileSync, writeFileSync } from 'fs';
const fileName = "../mit.json";
const fileData = readFileSync(fileName, "utf8");

import LZMA_web from 'lzma-web'
const LZMA = LZMA_web.default
const lzma = new LZMA()

console.log("Compressing...");
console.log("Compressing... initial stage...");
const compressed = await lzma.compress(fileData)

await lzma.cb.compress(
	fileData, 
	9, // compression level must be set when using callback
	(result, error) => { // when the compression finishes or errors
		if (error) throw error
		console.log("Completed. Writing to file.");
		const output = Uint8Array.from(result);
		writeFileSync('../mit.json.lzma', output)
	},
	(progressPercentage) => {
		console.log(`Compressing... ${(progressPercentage*100).toFixed(2)}`);
	},
)
