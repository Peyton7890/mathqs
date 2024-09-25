# MathQs

## Author: Peyton Martin

MathQS is a FastAPI web application that allows users to generate custom math tests based on user-defined problem counts. The application compiles the problems and solutions into LaTeX documents, converts them to PDF format, and provides download links for the generated tests.

## Requirements

Before running the code, make sure you have Python installed on your system. You will also need to install the following packages:

1. **SymPy**: For symbolic mathematics.
2. **LaTeX**: For generating and compiling LaTeX documents (e.g., TeX Live, MikTeX).
3. **FastAPI**: For building the web application
4. **Uvicorn**: For running asynchronous web applications in Python
5. **Jinja2**: For rendering HTML templates dynamically

### Installation Instructions

1. **Install Python Modules**:

   You can install the correct python modules using using pip: "pip install sympy fastapi uvicorn jinja2"

2. **Install LaTeX**:

    - **For Windows**: Install MikTeX from [miktex.org](https://miktex.org/download).
    - **For macOS**: Install MacTeX from [tug.org/mactex](https://tug.org/mactex/).
    - **For Linux**: Install TeX Live using your package manager, e.g., for Ubuntu: "sudo apt-get install texlive-full"

3. **Verify Installation**:

    Ensure that you can run `pdflatex` from the command line: "pdflatex --version"

## Running the Code

1. **Clone the Repository**:

    Clone this repository to your local machine: "git clone <https://github.com/Peyton7890/MathTestCreator.git>"

2. **Run the Code**:

    Start the FastAPI server script: "uvicorn app:app --reload"

3. **Use the Site**:

    Open your web browser and navigate to http://127.0.0.1:8000

    Fill out the form to specify the number of problems for each type and click the Generate Test button.

    After the PDFs are generated, download links for both the problems and solutions will be displayed.

4. **Stop the Code**:

    Press ctl+c to stop the server

## Directory Structure

    mathqs/

    │

    ├── app.py                   # FastAPI application

    ├── CalcProblemGenerator.py      # Problem generation logic

    ├── TestGenerator.py         # Test generation logic

    ├── templates/               # HTML templates

    │   └── index.html           # Main template for the web app

    ├── public/                  # Directory for generated PDF files

    ├── static/                  # Directory for static files (e.g., CSS)

    └── README.md                # Project documentation
