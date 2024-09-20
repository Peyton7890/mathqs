# CalcProblemGenerator.py
# Author: Peyton Martin
# Description: This module generates various types of calculus problems and their solutions, 
# including derivatives, integrals, and more complex topics such as U-substitution and integration by parts.


import random
import sympy as sp

# Define symbols for calculus problems
x, n, a = sp.symbols('x n a')

# List of functions for derivatives and integrals
basic_functions = [
    sp.sin(x), sp.cos(x), sp.tan(x), sp.sec(x), sp.csc(x), sp.cot(x),
    sp.exp(x), sp.ln(x), sp.log(x, 10), sp.asin(x), sp.acos(x), sp.atan(x),
    sp.sqrt(x), sp.root(x, 3), 1/x, x**2, x**3, x**(-1), x**(-2),
    sp.cos(sp.pi * x), sp.sin(sp.pi * x),
    sp.exp(-x), 1/(x + 1), 1/(x**2 + 1),
    sp.sin(x)*sp.cos(x), sp.exp(sp.sin(x)), sp.log(sp.sqrt(x)),
]

def generate_derivative():
    """
    Generate a derivative problem and its solution.

    Returns:
        tuple: A tuple containing the problem statement and the solution.
    """
    func = random.choice(basic_functions)
    problem = f"Find the derivative of: ${sp.latex(func)}$"
    solution = f"\\[ {sp.latex(sp.diff(func, x))} \\]"
    return problem, solution

def generate_integral():
    """
    Generate an integral problem and its solution.

    Returns:
        tuple: A tuple containing the problem statement and the solution.
    """
    func = random.choice(basic_functions)
    problem = f"Find the integral of: ${sp.latex(func)}$"
    solution = f"\\[ {sp.latex(sp.integrate(func, x))} + C \\]"
    return problem, solution

def generate_u_substitution():
    """
    Generate a U-substitution integral problem and its solution.

    Returns:
        tuple: A tuple containing the problem statement and the solution.
    """
    func = random.choice([sp.sin(2*x), sp.exp(2*x), (2*x + 1)**3])
    problem = f"Use U-substitution to find the integral of: ${sp.latex(func)}$"
    solution = f"\\[ {sp.latex(sp.integrate(func, x))} + C \\]"
    return problem, solution

def generate_integration_by_parts():
    """
    Generate an integration by parts problem and its solution.

    Returns:
        tuple: A tuple containing the problem statement and the solution.
    """
    func = random.choice([x * sp.exp(x), x * sp.ln(x)])
    problem = f"Use integration by parts to find the integral of: ${sp.latex(func)}$"
    solution = f"\\[ {sp.latex(sp.integrate(func, x))} + C \\]"
    return problem, solution

def generate_trigonometric_integral():
    """
    Generate a trigonometric integral problem and its solution.

    Returns:
        tuple: A tuple containing the problem statement and the solution.
    """
    func = random.choice([sp.sin(x)**2, sp.cos(x)**2, sp.sin(x)*sp.cos(x)])
    problem = f"Find the integral of the trigonometric function: ${sp.latex(func)}$"
    solution = f"\\[ {sp.latex(sp.integrate(func, x))} + C \\]"
    return problem, solution

def generate_trigonometric_substitution():
    """
    Generate a trigonometric substitution problem and its solution.

    Returns:
        tuple: A tuple containing the problem statement and the solution.
    """
    func = random.choice([sp.sqrt(1 - x**2), sp.sqrt(x**2 - 1)])
    problem = f"Use trigonometric substitution to find the integral of: ${sp.latex(func)}$"
    solution = f"\\[ {sp.latex(sp.integrate(func, x))} + C \\]"
    return problem, solution

def generate_partial_fractions():
    """
    Generate a partial fractions problem and its solution.

    Returns:
        tuple: A tuple containing the problem statement and the solution.
    """
    func = random.choice([1/(x*(x+1)), 1/(x**2 + 1)])
    problem = f"Use partial fractions to find the integral of: ${sp.latex(func)}$"
    solution = f"\\[ {sp.latex(sp.integrate(func, x))} + C \\]"
    return problem, solution

def generate_improper_integral():
    """
    Generate an improper integral problem and its solution.

    Returns:
        tuple: A tuple containing the problem statement and the solution.
    """
    func = random.choice([1/(x**2), 1/(x**2 + 1)])
    problem = f"Find the improper integral of: ${sp.latex(func)}$ from $1$ to $\\infty$"
    solution = f"\\[ {sp.latex(sp.integrate(func, (x, 1, sp.oo)))} \\]"
    return problem, solution

def generate_limit():
    """
    Generate a limit problem and its solution.

    Returns:
        tuple: A tuple containing the problem statement and the solution.
    """
    func = random.choice(basic_functions)
    point = random.choice([0, 1, sp.oo])
    problem = f"Find the limit of: ${sp.latex(func)}$ as $x$ approaches ${sp.latex(point)}$"
    solution = f"\\[ {sp.latex(sp.limit(func, x, point))} \\]"
    return problem, solution

def generate_series():
    """
    Generate a series problem and its solution.

    Returns:
        tuple: A tuple containing the problem statement and the solution.
    """
    func = random.choice([x**n/sp.factorial(n), x**n])
    problem = f"Find the sum of the series: $\\sum_{{n=0}}^{{\\infty}} {sp.latex(func)}$"
    solution = f"\\[ {sp.latex(sp.summation(func, (n, 0, sp.oo)))} \\]"
    return problem, solution

# Mapping of problem types to functions
problem_generators = {
    'derivative': generate_derivative,
    'integral': generate_integral,
    'u_substitution': generate_u_substitution,
    'integration_by_parts': generate_integration_by_parts,
    'trig_integral': generate_trigonometric_integral,
    'trig_substitution': generate_trigonometric_substitution,
    'partial_fractions': generate_partial_fractions,
    'improper_integral': generate_improper_integral,
    'limit': generate_limit,
    'series': generate_series,
}
