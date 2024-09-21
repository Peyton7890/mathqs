import os
import sys
import json
import subprocess
from TestGenerator import generate_problems_latex,  generate_solutions_latex
from TestGenerator import compile_latex_to_pdf, generate_custom_calculus_test

def delete_intermediate_files(filenames):
    """Delete specified intermediate files."""
    for filename in filenames:
        try:
            os.remove(filename)
        except FileNotFoundError:
            pass  # If the file doesn't exist, ignore the error

def main():
    # Parse the arguments passed from the Node.js backend
    problem_counts = json.loads(sys.argv[1])
    problems_output_path = sys.argv[2]
    solutions_output_path = sys.argv[3]

    # Generate test problems based on input problem counts
    test_problems = generate_custom_calculus_test(problem_counts)

    # Generate LaTeX file for problems
    problems_latex_filename = "calculus_problems.tex"
    generate_problems_latex(test_problems, filename=problems_latex_filename)
    compile_latex_to_pdf(problems_latex_filename)
    subprocess.run(["mv", "calculus_problems.pdf", problems_output_path])

    # Generate LaTeX file for solutions
    solutions_latex_filename = "calculus_solutions.tex"
    generate_solutions_latex(test_problems, filename=solutions_latex_filename)
    compile_latex_to_pdf(solutions_latex_filename)
    subprocess.run(["mv", "calculus_solutions.pdf", solutions_output_path])

    # List of intermediate files to delete
    intermediate_files = [
        problems_latex_filename,
        "calculus_problems.aux",
        "calculus_problems.log",
        solutions_latex_filename,
        "calculus_solutions.aux",
        "calculus_solutions.log"
    ]
    
    # Delete intermediate files
    delete_intermediate_files(intermediate_files)

if __name__ == "__main__":
    main()
