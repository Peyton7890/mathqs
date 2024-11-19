// Author: Peyton Martin
// Description: Frontend Lambda function that serves the HTML interface
// Functions:
//   - Reads and serves the HTML file
//   - Replaces placeholder API URL with environment variable

const fs = require('fs');
const path = require('path');

// Read HTML file and replace the API URL placeholder
const html = fs.readFileSync(path.join(__dirname, 'index.html'), 'utf8')
    .replace('BACKEND_API_URL', process.env.BACKEND_API_URL);

// Lambda handler function
exports.handler = async (event) => {
    // Return HTML with proper headers
    return {
        statusCode: 200,
        headers: {
            'Content-Type': 'text/html',
        },
        body: html
    };
};