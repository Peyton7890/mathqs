################################
# Lambda Functions Configuration
# Purpose: Defines serverless compute resources
#
# Resources:
# - ECR Repository: Hosts Docker image for backend
# - Backend Lambda: PDF generation (Docker container)
#   - Memory: 1024MB
#   - Timeout: 30 seconds
#   - Storage: 512MB
# - Frontend Lambda: Serves web interface
#   - Runtime: Node.js 18.x
#   - Environment: Configured with backend URL
################################

# ECR repository for Lambda container
resource "aws_ecr_repository" "mathqs_lambda" {
  name = "mathqs-lambda"
  force_delete = true
}

# Backend Lambda function
resource "aws_lambda_function" "mathqs_lambda" {
  function_name    = "mathqs_lambda"
  package_type     = "Image"
  image_uri        = "${aws_ecr_repository.mathqs_lambda.repository_url}:latest"
  role             = aws_iam_role.lambda_role.arn

  memory_size      = 1024  # Increase memory
  timeout          = 30    # Increase timeout
  ephemeral_storage {
    size = 512  # Increase /tmp storage
  }
}

# Frontend Lambda function
resource "aws_lambda_function" "frontend_lambda" {
  filename         = "frontend/frontend_lambda.zip"
  function_name    = "mathqs_frontend"
  handler          = "index.handler"
  runtime          = "nodejs18.x"
  role            = aws_iam_role.frontend_lambda_role.arn

  environment {
    variables = {
      BACKEND_API_URL = "${aws_apigatewayv2_stage.mathqs_stage.invoke_url}/generate"
    }
  }
}