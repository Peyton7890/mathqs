import { NextRequest, NextResponse } from 'next/server';
import { exec } from 'child_process';
import path from 'path';

// Define the paths to the Python script and output PDFs
const pythonScriptPath = path.join(process.cwd(), 'scripts', 'generate_problems.py');
const problemsOutputPath = path.join(process.cwd(), 'public', 'calculus_problems.pdf');
const solutionsOutputPath = path.join(process.cwd(), 'public', 'calculus_solutions.pdf');

export async function POST(req: NextRequest): Promise<Response> {
  try {
    const problemCounts = await req.json();

    console.log("Received problem counts:", problemCounts);
    console.log("Python script path:", pythonScriptPath);

    // Construct the command to execute
    const command = `python3 ${pythonScriptPath} '${JSON.stringify(problemCounts)}' '${problemsOutputPath}' '${solutionsOutputPath}'`;
    
    // Log the command being executed
    console.log(`Executing command: ${command}`);

    // Execute the command
    const result = await new Promise<string>((resolve, reject) => {
      exec(command, (error, stdout, stderr) => {
        if (error) {
          console.error(`exec error: ${error}`);
          console.error(`stderr: ${stderr}`);
          return reject(new Error('Error generating PDFs'));
        }
        console.log(`stdout: ${stdout}`);
        resolve(stdout);
      });
    });

    // Define URLs for the generated PDFs
    const pdfUrls = {
      problems: '/calculus_problems.pdf',
      solutions: '/calculus_solutions.pdf',
    };
    console.log("PDF URLs:", pdfUrls);
    
    // Return the URLs in the response
    return NextResponse.json(pdfUrls);

  } catch (error) {
    console.error(`Error processing request: ${error}`);
    return NextResponse.json({ error: 'Error processing request' }, { status: 500 });
  }
}
