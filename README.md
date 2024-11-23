# MathQ's

## Author: Peyton Martin

A serverless calculus test generator that creates customized calculus problems and generates downloadable PDFs of both problems and solutions.

Visit: <https://mathqs.com>

## Features

- Interactive web interface for customizing test content
- Support for multiple calculus problem types:
  - Derivatives
  - Integrals
  - U-Substitution
  - Integration by Parts
  - Trigonometric Integrals
  - Trigonometric Substitution
  - Partial Fractions
  - Improper Integrals
  - Limits
  - Series
- Automatic generation of both problem and solution PDFs

## Architecture

- **Frontend**: 
  - Static HTML/JS served via Lambda
  - Clean, responsive interface
  - Real-time problem count selection

- **Backend**:
  - Python-based Lambda using Docker
  - Matplotlib for PDF generation
  - SymPy for mathematical expressions

- **Infrastructure**:
  - API Gateway for HTTP endpoints
  - Route53 for custom domain
  - S3 for PDF storage
  - ECR for Docker image hosting
  - Terraform for infrastructure as code

##

### Prerequisites

- AWS CLI configured with appropriate permissions
- Terraform >= 1.0
- Docker installed and configured
- Python 3.12
- Node.js 18.x (for frontend Lambda)

### Deployment

1. Clone the repository
2. Navigate to the scripts directory and run the deployment script:

```bash
(cd scripts && ./deploy.sh)
```

This will:

- Package the frontend and backend Lambda functions
- Create the backend dependencies layer and package it
- Deploy all AWS infrastructure via Terraform

### Teardown

To remove all deployed resources and clean up the directory, run:

```bash
(cd scripts && ./destroy.sh)
```

This will delete the Lambda function, associated IAM roles, and any other related resources created by the deployment.
