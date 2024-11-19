# Author: Peyton Martin
# Description: Defines S3 buckets for MathQs application
# Resources:
#   - Public S3 bucket for storing generated PDFs
#   - Private S3 bucket for Lambda layers
#   - Bucket policies and access controls

# Public bucket for storing generated PDF files
resource "aws_s3_bucket" "files_bucket" {
  bucket = "mathqs"
  force_destroy = true
}

# Configure public access settings for the files bucket
resource "aws_s3_bucket_public_access_block" "files_bucket_public_access" {
  bucket = aws_s3_bucket.files_bucket.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "files_bucket_policy" {
  bucket = aws_s3_bucket.files_bucket.id
  depends_on = [aws_s3_bucket_public_access_block.files_bucket_public_access]

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.files_bucket.arn}/*"
      },
    ]
  })
}

resource "aws_s3_bucket_ownership_controls" "files_bucket_ownership" {
  bucket = aws_s3_bucket.files_bucket.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_acl" "files_bucket_acl" {
  depends_on = [
    aws_s3_bucket_ownership_controls.files_bucket_ownership,
    aws_s3_bucket_public_access_block.files_bucket_public_access,
  ]

  bucket = aws_s3_bucket.files_bucket.id
  acl    = "public-read"
}

# Private bucket for storing Lambda layers
resource "aws_s3_bucket" "mathqs_lambda_bucket" {
  bucket = "mathqs-lambda-layer-bucket"
}

resource "aws_s3_object" "lambda_layer_object" {
  bucket = aws_s3_bucket.mathqs_lambda_bucket.bucket
  key    = "lambda_layer.zip"
  source = "lambda/lambda_layer.zip"
  acl    = "private"
}