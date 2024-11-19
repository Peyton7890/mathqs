# Author: Peyton Martin
# Description: Defines Lambda functions for the MathQs application
# Resources:
#   - Backend Lambda function and layer for PDF generation
#   - Frontend Lambda function for serving web interface

# Backend Lambda layer
resource "aws_lambda_layer_version" "mathqs_lambda_layer" {
  layer_name          = "mathqs_lambda_layer"
  compatible_runtimes = ["python3.12"]

  s3_bucket = aws_s3_bucket.mathqs_lambda_bucket.bucket
  s3_key    = aws_s3_object.lambda_layer_object.key
}

# Backend Lambda function
resource "aws_lambda_function" "mathqs_lambda" {
  filename         = "lambda/lambda.zip"
  function_name    = "mathqs_lambda"
  handler          = "lambda_function.handler" 
  runtime          = "python3.12"
  role             = aws_iam_role.lambda_role.arn

  layers = [
    aws_lambda_layer_version.mathqs_lambda_layer.arn,
  ]

  memory_size      = 256
  timeout          = 30
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