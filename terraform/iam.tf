# Author: Peyton Martin
# Description: Defines IAM roles and policies
# Resources:
#   - Backend Lambda execution role and policies
#   - Frontend Lambda execution role and policies

## Backend IAM resources ##

# Create Lambda execution role
resource "aws_iam_role" "lambda_role" {
  name = "lambda_execution_role"
  assume_role_policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": "sts:AssumeRole",
        "Effect": "Allow",
        "Principal": {
          "Service": "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# Create policy for S3 access
resource "aws_iam_policy" "s3_put_policy" {
  name        = "lambda_s3_put_policy"
  description = "Allow Lambda function to put objects in the mathqs S3 bucket"
  policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": "s3:PutObject",
        "Resource": "arn:aws:s3:::mathqs/*"
      }
    ]
  })
}

# Attach S3 policy to Lambda execution role
resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "lambda_s3_put_policy_attachment" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.s3_put_policy.arn
}

## Backend IAM resources ##
# Frontend Lambda IAM role
resource "aws_iam_role" "frontend_lambda_role" {
  name = "frontend_lambda_execution_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "frontend_lambda_basic_execution" {
  role       = aws_iam_role.frontend_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}
