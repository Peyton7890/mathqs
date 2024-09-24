import { NextRequest, NextResponse } from 'next/server';
import { exec } from 'child_process';
import path from 'path';

// Define the paths to the Python script and output PDFs
const pythonScriptPath = path.join(process.cwd(), 'scripts', 'generate_problems.py');
const problemsOutputPath = path.join(process.cwd(), 'public', 'calculus_problems.pdf');
const solutionsOutputPath = path.join(process.cwd(), 'public', 'calculus_solutions.pdf');

export async function POST(req: NextRequest): Promise<Response> {
  const problemCounts = await req.json();

  console.log("Received problem counts:", problemCounts);
  console.log("Python script path:", pythonScriptPath);

  // Construct the command to execute
  const command = `python3 ${pythonScriptPath} '${JSON.stringify(problemCounts)}' '${problemsOutputPath}' '${solutionsOutputPath}'`;
  
  // Log the command being executed
  console.log(`Executing command: ${command}`);

  return new Promise((resolve) => {
    exec(command, (error) => {
      if (error) {
        console.error(`exec error: ${error}`);
        return resolve(
          NextResponse.json({ error: 'Error generating PDFs' }, { status: 500 })
        );
      }

      const pdfUrls = {
        problems: '/calculus_problems.pdf',
        solutions: '/calculus_solutions.pdf',
      };
      console.log("PDF URLs:", pdfUrls);
      resolve(NextResponse.json(pdfUrls));
    });
  });
}
