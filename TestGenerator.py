# TestGenerator.py
# Author: Peyton Martin
# Description: This module generates a custom calculus test based on user-defined problem counts
# and compiles the problems and solutions into LaTeX documents, which are then converted to PDF.


import subprocess
import os
from CalcProblemGenerator import calc_problem_generators

# Example of user input to specify problem counts for each type
problem_counts = {
    'derivative': 1,
    'integral': 1,
    'u_substitution': 1,
    'integration_by_parts': 1,
    'trig_integral': 1,
    'trig_substitution': 1,
    'partial_fractions': 1,
    'improper_integral': 1,
    'limit': 1,
    'series': 1,
}

def generate_custom_calculus_test(problem_counts):
    """
    Generate a custom calculus test based on specified problem counts.

    Args:
        problem_counts (dict): A dictionary where keys are problem types
                               and values are the number of problems to generate.

    Returns:
        list: A list of tuples containing the problems and their solutions.
    """
    test_problems = []

    # Loop through the problem types and generate the specified number of problems
    for problem_type, count in problem_counts.items():
        if problem_type in calc_problem_generators:
            for _ in range(count):
                problem_func = calc_problem_generators[problem_type]
                problem, solution = problem_func()
                test_problems.append((problem, solution))
    
    return test_problems

def generate_problems_latex(test_problems, filename="calculus_problems.tex"):
    """
    Generate a LaTeX document for the problems.

    Args:
        test_problems (list): A list of tuples containing the problems and their solutions.
        filename (str): The filename for the output LaTeX document.

    Returns:
        str: The filename of the generated LaTeX document.
    """
    header = r"""\documentclass{article}
\usepackage{amsmath, amssymb}
\usepackage[margin=1in]{geometry}
\begin{document}
\title{Custom Calculus Test Problems}
\author{}
\date{}
\maketitle
"""

    footer = r"\end{document}"

    # Create LaTeX for problems only
    problems_content = ""
    for i, (problem, _) in enumerate(test_problems, 1):
        problems_content += f"\\section*{{Problem {i}}}\n"
        problems_content += f"{problem}\n\n"
        problems_content += "\\vfill\n"

        # Add a new page every two problems
        if i % 2 == 0:
            problems_content += "\\newpage\n"
        else:
            problems_content += "\\vfill\n"  # Half page spacing for the second problem

    # Combine everything into a full LaTeX document
    latex_document = header + problems_content + footer

    # Write to a .tex file
    with open(filename, 'w') as f:
        f.write(latex_document)
    
    print(f"LaTeX document for problems saved as {filename}.")
    
    return filename

def generate_solutions_latex(test_problems, filename="calculus_solutions.tex"):
    """
    Generate a LaTeX document for the solutions.

    Args:
        test_problems (list): A list of tuples containing the problems and their solutions.
        filename (str): The filename for the output LaTeX document.

    Returns:
        str: The filename of the generated LaTeX document.
    """
    header = r"""\documentclass{article}
\usepackage{amsmath, amssymb}
\usepackage[margin=1in]{geometry}
\begin{document}
\title{Custom Calculus Test Solutions}
\author{}
\date{}
\maketitle
"""

    footer = r"\end{document}"

    # Create LaTeX for solutions
    solutions_content = ""
    for i, (problem, solution) in enumerate(test_problems, 1):
        solutions_content += f"\\section*{{Solution to Problem {i}}}\n"
        solutions_content += f"{problem}\n\n"
        solutions_content += f"{solution}\n\n"

    # Combine everything into a full LaTeX document
    latex_document = header + solutions_content + footer

    # Write to a .tex file
    with open(filename, 'w') as f:
        f.write(latex_document)
    
    print(f"LaTeX document for solutions saved as {filename}.")
    
    return filename

def compile_latex_to_pdf(latex_filename):
    """
    Compile a LaTeX file into a PDF using pdflatex.

    Args:
        latex_filename (str): The filename of the LaTeX document to compile.
    """
    try:
        # Use subprocess to call pdflatex and generate the PDF
        subprocess.run(['pdflatex', latex_filename], check=True)
        print(f"PDF generated from {latex_filename}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while compiling LaTeX: {e}")

# Generate test problems
test_problems = generate_custom_calculus_test(problem_counts)

# Generate the LaTeX documents
problems_filename = generate_problems_latex(test_problems, filename="calculus_problems.tex")
solutions_filename = generate_solutions_latex(test_problems, filename="calculus_solutions.tex")

# Compile the LaTeX documents into PDFs
compile_latex_to_pdf(problems_filename)
compile_latex_to_pdf(solutions_filename)

# Clean up auxiliary files generated by pdflatex
auxiliary_extensions = ['aux', 'log', 'out']
for ext in auxiliary_extensions:
    try:
        os.remove(problems_filename.replace('.tex', f'.{ext}'))
        os.remove(solutions_filename.replace('.tex', f'.{ext}'))
    except FileNotFoundError:
        pass
