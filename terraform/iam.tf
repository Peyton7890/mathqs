################################
# IAM Configuration
# Purpose: Manages IAM roles and policies for Lambda functions
#
# Components:
# 1. Backend Lambda Role
#    - Basic Lambda execution
#    - S3 access for PDF storage
#    - ECR access for container image
#
# 2. Frontend Lambda Role
#    - Basic Lambda execution
#    - Environment variable access
#
# Policies:
# - Custom S3 policy for PDF operations
# - ECR pull permissions for container
# - CloudWatch logging permissions
################################

## Backend IAM resources ##

# Backend Lambda IAM role
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
        "Action": [
          "s3:PutObject",
          "s3:PutObjectAcl"
        ],
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

# Add ECR pull permissions
resource "aws_iam_role_policy_attachment" "lambda_ecr_policy" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

## Frontend IAM resources ##
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
