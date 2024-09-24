from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import subprocess
import os
import json

app = FastAPI()

@app.post("/generate")
async def generate_problems(request: Request):
    # Parse the incoming JSON payload
    problem_counts = await request.json()

    # Define paths for the output PDFs
    problems_output_path = os.path.join(os.getcwd(), 'public', 'calculus_problems.pdf')
    solutions_output_path = os.path.join(os.getcwd(), 'public', 'calculus_solutions.pdf')
    python_script_path = os.path.join(os.getcwd(), 'scripts', 'generate_problems.py')

    # Run the Python script with problem counts
    try:
        subprocess.run(
            ["python3", python_script_path, json.dumps(problem_counts), problems_output_path, solutions_output_path],
            check=True
        )
    except subprocess.CalledProcessError as e:
        return JSONResponse(status_code=500, content={"error": "Failed to generate PDFs"})

    # Return URLs for both problems and solutions PDFs
    return {
        "problems": "/calculus_problems.pdf",
        "solutions": "/calculus_solutions.pdf"
    }
