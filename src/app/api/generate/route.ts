import { NextRequest, NextResponse } from 'next/server';
import { exec } from 'child_process';
import path from 'path';

export async function POST(req: NextRequest): Promise<Response> {
  const problemCounts = await req.json();

  // Define the paths to the Python script and output PDFs
  const pythonScriptPath = path.join(process.cwd(), 'api', 'generate_problems.py');
  const problemsOutputPath = path.join(process.cwd(), 'public', 'calculus_problems.pdf');
  const solutionsOutputPath = path.join(process.cwd(), 'public', 'calculus_solutions.pdf');

  console.log("Received problem counts:", problemCounts);
  console.log("Python script path:", pythonScriptPath);

  return new Promise((resolve) => {
    exec(`python ${pythonScriptPath} '${JSON.stringify(problemCounts)}' '${problemsOutputPath}' '${solutionsOutputPath}'`, (error) => {
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
