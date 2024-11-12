resource "aws_s3_bucket" "files_bucket" {
  bucket = "mathqs"
  force_destroy = true
}

resource "aws_s3_bucket" "mathqs_lambda_bucket" {
  bucket = "mathqs-lambda-layer-bucket"
}

resource "aws_s3_object" "lambda_layer_object" {
  bucket = aws_s3_bucket.mathqs_lambda_bucket.bucket
  key    = "lambda_layer.zip"
  source = "lambda/lambda_layer.zip"
  acl    = "private"
}

resource "aws_lambda_layer_version" "mathqs_lambda_layer" {
  layer_name          = "mathqs_lambda_layer"
  compatible_runtimes = ["python3.12"]

  s3_bucket = aws_s3_bucket.mathqs_lambda_bucket.bucket
  s3_key    = aws_s3_object.lambda_layer_object.key
}

resource "aws_lambda_function" "my_lambda_function" {
  filename         = "lambda/lambda.zip"
  function_name    = "my_lambda_function"
  handler          = "lambda_function.handler"  # Update with the handler function
  runtime          = "python3.12"
  role             = aws_iam_role.lambda_role.arn

  layers = [
    aws_lambda_layer_version.mathqs_lambda_layer.arn,
  ]

  memory_size      = 256
  timeout          = 30
}