# TestGenerator.py
# Author: Peyton Martin
# Description: This module generates a custom calculus test based on user-defined problem counts
# and compiles the problems and solutions into LaTeX documents, which are then converted to PDF.

import subprocess
import tempfile
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
    unique_problems = set()  # Set to keep track of unique problems

    # Loop through the problem types and generate the specified number of problems
    for problem_type, count in problem_counts.items():
        if problem_type in calc_problem_generators:
            attempts = 0  # Track the number of attempts for each type
            generated_count = 0  # Track how many unique problems have been generated

            while generated_count < count:
                problem_func = calc_problem_generators[problem_type]
                problem, solution = problem_func()

                # Check for duplicates using the unique_problems set
                if problem not in unique_problems:
                    unique_problems.add(problem)  # Add to the set of unique problems
                    test_problems.append((problem, solution))  # Append to the test problems list
                    generated_count += 1  # Increment the count of generated problems

                attempts += 1
                if attempts > 1000:  # Prevent infinite loops; adjust as needed
                    print(f"Warning: Too many attempts generating unique problems for '{problem_type}'.")
                    break

            # After attempting to generate, check if we achieved the desired count
            if generated_count < count:
                print(f"Warning: Only {generated_count} unique problems generated for '{problem_type}'.")

    return test_problems


def generate_problems_latex_content(test_problems):
    """
    Generate LaTeX content for the problems.

    Args:
        test_problems (list): A list of tuples containing the problems and their solutions.

    Returns:
        str: The LaTeX content of the problems.
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

    return header + problems_content + footer

def generate_solutions_latex_content(test_problems):
    """
    Generate LaTeX content for the solutions.

    Args:
        test_problems (list): A list of tuples containing the problems and their solutions.

    Returns:
        str: The LaTeX content of the solutions.
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

    return header + solutions_content + footer

def compile_latex_to_pdf(latex_content, pdf_filename):
    """
    Compile LaTeX content directly into a PDF using pdflatex without creating auxiliary files.

    Args:
        latex_content (str): The LaTeX content to compile.
        pdf_filename (str): The filename for the output PDF file.
    """
    try:
        # Create a temporary directory to store all intermediate files, which will be deleted automatically
        with tempfile.TemporaryDirectory() as tmpdirname:
            # Use subprocess to call pdflatex and pipe LaTeX content
            process = subprocess.run(
                ['pdflatex', '-output-directory', tmpdirname, '-jobname', pdf_filename.replace('.pdf', '')],
                input=latex_content.encode('utf-8'),
                check=True, capture_output=True
            )
            
            # Move the resulting PDF to the desired location
            tmp_pdf_path = os.path.join(tmpdirname, pdf_filename)
            if os.path.exists(tmp_pdf_path):
                os.rename(tmp_pdf_path, pdf_filename)
                print(f"PDF generated as {pdf_filename}")
            else:
                print(f"PDF was not generated properly.")
    
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while compiling LaTeX: {e}")



########################
def main():
    """
    Main function to test the generation of custom calculus test PDFs.
    It generates both the problem and solution PDFs and ensures no intermediate files are created.
    """

    # Define the problem counts for each type of calculus problem
    p_counts = {
        'derivative': 20,
        'integral': 20,
        'u_substitution': 1,
        'integration_by_parts': 1,
        'trig_integral': 1,
        'trig_substitution': 1,
        'partial_fractions': 1,
        'improper_integral': 1,
        'limit': 1,
        'series': 1,
    }

    # Generate custom calculus test problems based on problem counts
    print("Generating calculus test problems...")
    test_problems = generate_custom_calculus_test(p_counts)

    # Generate and test the problems PDF
    print("Generating problems PDF...")
    compile_latex_to_pdf(generate_problems_latex_content(test_problems), "calculus_problems_test.pdf")
    print("Problems PDF generated successfully: calculus_problems_test.pdf")

    # Generate and test the solutions PDF
    print("Generating solutions PDF...")
    compile_latex_to_pdf(generate_solutions_latex_content(test_problems), "calculus_problems_solutions.pdf")
    print("Solutions PDF generated successfully: calculus_solutions_test.pdf")

if __name__ == "__main__":
    main()
