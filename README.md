# MathTestCreator

## Author: Peyton Martin

This project consists of two Python modules that generate various types of calculus problems and their solutions, including derivatives, integrals, and more complex topics. The problems are formatted into LaTeX documents and compiled into PDF files.

## Requirements

Before running the code, make sure you have Python installed on your system. You will also need to install the following packages:

1. **SymPy**: For symbolic mathematics.
2. **LaTeX**: For generating and compiling LaTeX documents (e.g., TeX Live, MikTeX).
3. **subprocess**: This is included in Python's standard library, so no installation is needed.

### Installation Instructions

1. **Install SymPy**:

   You can install SymPy using pip: "pip install sympy"

2. **Install LaTeX**:

    - **For Windows**: Install MikTeX from [miktex.org](https://miktex.org/download).
    - **For macOS**: Install MacTeX from [tug.org/mactex](https://tug.org/mactex/).
    - **For Linux**: Install TeX Live using your package manager, e.g., for Ubuntu: "sudo apt-get install texlive-full"

3. **Verify Installation**:

Ensure that you can run `pdflatex` from the command line: "pdflatex --version"

## Running the Code

1. **Clone the Repository**:

    Clone this repository to your local machine: "git clone <https://github.com/Peyton7890/MathTestCreator.git>"

2. **Modify Problem Counts**:

    Open `TestGenerator.py` and adjust the `problem_counts` dictionary to specify how many problems of each type you want to generate.

3. **Run the Code**:

Execute the `TestGenerator.py` script: "python3 TestGenerator.py"

This will generate LaTeX files for both problems and solutions, compile them into PDF files, and clean up any auxiliary files created during compilation.

## Output

The generated PDF files will be named `calculus_problems.pdf` and `calculus_solutions.pdf`.

## License

This project is licensed under the MIT License.
