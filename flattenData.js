const fs = require('fs');

const flattenedData = [];
const jsonData = require('./index_0.json');

for (const [filename, data] of Object.entries(jsonData)) {
  flattenedData.push({ filename, ...data });
}

// Convert the array to a JSON string
const flatJSON = JSON.stringify(flattenedData, null, 2); // The third parameter (2) is for indentation (optional)

// Specify the file path
const filePath = 'flatData.json';

// Write the JSON data to the file
fs.writeFile(filePath, flatJSON, 'utf8', (err) => {
  if (err) {
    console.error('Error writing JSON file:', err);
  } else {
    console.log('JSON file has been written successfully:', filePath);
  }
});