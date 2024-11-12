# TestGenerator.py
# Author: Peyton Martin
# Description: Generates a custom calculus test with problems and solutions using Matplotlib for PDF.

import matplotlib.pyplot as plt
import sympy as sp
from CalcProblemGenerator import calc_problem_generators

def generate_custom_calculus_test(problem_counts):
    """
    Generate a custom calculus test based on specified problem counts.
    """
    test_problems = []
    unique_problems = set()

    for problem_type, count in problem_counts.items():
        if problem_type in calc_problem_generators:
            attempts = 0
            generated_count = 0

            while generated_count < count:
                problem_func = calc_problem_generators[problem_type]
                problem, solution = problem_func()

                if problem not in unique_problems:
                    unique_problems.add(problem)
                    test_problems.append((problem, solution))
                    generated_count += 1

                attempts += 1
                if attempts > 1000:
                    print(f"Warning: Too many attempts for '{problem_type}'.")
                    break

            if generated_count < count:
                print(f"Warning: Only {generated_count} unique problems for '{problem_type}'.")

    return test_problems

def render_math_expression(expression, is_solution=False):
    """
    Renders a mathematical expression in LaTeX format or returns it as plain text if it's not valid.
    """
    try:
        # If the expression is purely a math expression, render it with sympy
        sym_expr = sp.sympify(expression)
        # Use LaTeX format for rendering
        rendered_expr = sp.latex(sym_expr)
        # Use display math mode for solutions
        if is_solution:
            return f"$${rendered_expr}$$"  # Use display math mode
        else:
            return f"${rendered_expr}$"  # Inline math mode
    except Exception:
        return expression  # Return the expression as plain text if it fails

def save_problem_pdf(test_problems, pdf_filename="calculus_problems_test.pdf"):
    """
    Generate a PDF for the problems using Matplotlib.
    """
    plt.figure(figsize=(8, 11))
    plt.title("Calculus Test Problems", fontsize=16, pad=1)  # Increase title padding for extra space
    plt.axis('off')  # Turn off the axis

    # Start text placement lower down to add space between title and first problem
    start_y = 0.95

    for i, (problem, _) in enumerate(test_problems, 1):
        problem_text = render_math_expression(problem)  # Render problem
        plt.text(0.5, start_y - (i - 1) * 0.1, f"Problem {i}: {problem_text}", fontsize=12, ha='center')

    plt.savefig(pdf_filename, bbox_inches='tight')
    plt.close()
    print(f"Problems PDF generated as {pdf_filename}")

def save_solutions_pdf(test_problems, pdf_filename="calculus_solutions_test.pdf"):
    """
    Generate a PDF for the solutions using Matplotlib.
    """
    plt.figure(figsize=(8, 11))
    plt.title("Calculus Test Solutions", fontsize=16, pad=1) 
    plt.axis('off')  # Turn off the axis

    # Start text placement lower down to add space between title and first solution
    start_y = 0.95

    for i, (problem, solution) in enumerate(test_problems, 1):
        problem_text = render_math_expression(problem)
        solution_text = render_math_expression(solution, is_solution=True)

        # Adjust the text positioning
        plt.text(0.5, start_y - (i - 1) * 0.25, f"Solution to Problem {i}:", fontsize=12, ha='center')
        plt.text(0.5, start_y - (i - 1) * 0.25 - 0.05, f"Problem: {problem_text}", fontsize=12, ha='center')
        plt.text(0.5, start_y - (i - 1) * 0.25 - 0.1, f"Solution: {solution_text}", fontsize=12, ha='center')

    plt.savefig(pdf_filename, bbox_inches='tight')
    plt.close()
    print(f"Solutions PDF generated as {pdf_filename}")
