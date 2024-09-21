import { NextRequest, NextResponse } from 'next/server';
import { exec } from 'child_process';
import path from 'path';

export async function POST(req: NextRequest): Promise<Response> {
  const problemCounts = await req.json();

  // Define the paths to the Python script and output PDFs
  const pythonScriptPath = path.join(process.cwd(), 'scripts', 'generate_problems.py');
  const problemsOutputPath = path.join(process.cwd(), 'public', 'calculus_problems.pdf');
  const solutionsOutputPath = path.join(process.cwd(), 'public', 'calculus_solutions.pdf');

  return new Promise((resolve) => {
    exec(`python3 ${pythonScriptPath} '${JSON.stringify(problemCounts)}' '${problemsOutputPath}' '${solutionsOutputPath}'`, (error) => {
      if (error) {
        console.error(`exec error: ${error}`);
        return resolve(
          NextResponse.json({ error: 'Error generating PDFs' }, { status: 500 })
        );
      }

      // Return the URLs of the generated PDFs
      const pdfUrls = {
        problems: '/calculus_problems.pdf',
        solutions: '/calculus_solutions.pdf',
      };
      resolve(NextResponse.json(pdfUrls));
    });
  });
}
