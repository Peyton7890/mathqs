# MathQs

## Author: Peyton Martin

An AWS Lambda function that creates various types of calculus problems, compiles these problems into a customizable calculus test and generates a PDF document of the test along with its solutions.
  
## Setup and Deployment

The project is designed to run as an AWS Lambda function. You can deploy and manage the Lambda function with the provided shell scripts in the `scripts` directory.

### Prerequisites

- **AWS CLI** installed and configured with appropriate IAM permissions.
- **Terraform** installed to handle infrastructure deployment.
- **Python 3.12** with dependencies packaged for Lambda (e.g., `sympy`, `boto3`, `reportlab`, `matplotlib`, `Pillow`).

### Deployment

To deploy the Lambda function, navigate to the `scripts` folder and run:

```bash
./deploy.sh
```

This script will package the required files, create the necessary IAM roles, and deploy the Lambda function using Terraform.

### Teardown

To remove all deployed resources and tear down the Lambda function, run:

```bash
./destroy.sh
```

This will delete the Lambda function, associated IAM roles, and any other related resources created by the deployment.
