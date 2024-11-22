#!/bin/bash
################################
# MathQs Cleanup Script
# Author: Peyton Martin
#
# This script performs a complete cleanup:
# 1. Docker Cleanup
#    - Removes local images
#    - Cleans ECR images
#
# 2. AWS Infrastructure
#    - Destroys all Terraform-managed resources
#
# 3. Local Cleanup
#    - Removes build artifacts
#
# Requirements:
#   - AWS CLI configured
#   - Docker installed
#   - Terraform state accessible
################################

# Set Terraform directory path
TERRAFORM_DIR="../terraform"

# Get AWS account and region info
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
AWS_REGION=$(aws configure get region)
ECR_REPO="mathqs-lambda"
TAG="latest"

# Docker cleanup
echo "Removing Docker images..."
docker rmi $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:$TAG || true
docker rmi $ECR_REPO:$TAG || true

# AWS infrastructure cleanup
echo "Destroying AWS infrastructure..."
(cd "$TERRAFORM_DIR" && terraform destroy -auto-approve)

# Local file cleanup
echo "Cleaning up local files..."
rm -f "../terraform/lambda/lambda.zip"
rm -f "../terraform/lambda/lambda_layer.zip"
rm -f "../terraform/frontend/frontend_lambda.zip"

echo "Cleanup complete!"

