import os
import shutil
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from TestGenerator import generate_custom_calculus_test, generate_problems_latex, generate_solutions_latex, compile_latex_to_pdf

app = FastAPI()

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/public", StaticFiles(directory="public"), name="public")  # Serve PDFs from public directory

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "problems_pdf": None, "solutions_pdf": None})

@app.post("/generate/")
async def generate_test(
    request: Request,
    derivative: int = Form(0),
    integral: int = Form(0),
    u_substitution: int = Form(0),
    integration_by_parts: int = Form(0),
    trig_integral: int = Form(0),
    trig_substitution: int = Form(0),
    partial_fractions: int = Form(0),
    improper_integral: int = Form(0),
    limit: int = Form(0),
    series: int = Form(0),
):
    problem_counts = {
        'derivative': derivative,
        'integral': integral,
        'u_substitution': u_substitution,
        'integration_by_parts': integration_by_parts,
        'trig_integral': trig_integral,
        'trig_substitution': trig_substitution,
        'partial_fractions': partial_fractions,
        'improper_integral': improper_integral,
        'limit': limit,
        'series': series,
    }

    # Generate test problems
    test_problems = generate_custom_calculus_test(problem_counts)

    # Generate the LaTeX documents
    problems_filename = generate_problems_latex(test_problems, filename="calculus_problems.tex")
    solutions_filename = generate_solutions_latex(test_problems, filename="calculus_solutions.tex")

    # Compile the LaTeX documents into PDFs
    compile_latex_to_pdf(problems_filename)
    compile_latex_to_pdf(solutions_filename)

    # Move PDFs to public folder
    shutil.move("calculus_problems.pdf", "public/calculus_problems.pdf")
    shutil.move("calculus_solutions.pdf", "public/calculus_solutions.pdf")

    # Delete the temporary files
    for filename in [problems_filename, solutions_filename, "calculus_problems.aux", "calculus_problems.log", "calculus_solutions.aux", "calculus_solutions.log"]:
        if os.path.exists(filename):
            os.remove(filename)

    # Render the homepage with download links
    return templates.TemplateResponse("index.html", {
        "request": request,
        "problems_pdf": "/public/calculus_problems.pdf",
        "solutions_pdf": "/public/calculus_solutions.pdf"
    })

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = f"public/{filename}"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        return {"error": "File not found."}
