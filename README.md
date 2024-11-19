# MathQs

## Author: Peyton Martin

A serverless calculus test generator that creates customized calculus problems and generates downloadable PDFs of both problems and solutions.

## Architecture

- **Frontend**: Serverless web interface hosted via AWS Lambda + API Gateway
- **Backend**: Python-based Lambda function that generates math problems and PDFs
- **Storage**: S3 buckets for storing generated PDFs and Lambda layers
- **Infrastructure**: Managed with Terraform

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
- Public URLs for easy access to generated documents

## Prerequisites

- AWS CLI configured with appropriate permissions
- Terraform >= 1.0
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
