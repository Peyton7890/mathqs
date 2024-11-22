#!/bin/bash
################################
# MathQs Deployment Script
# Author: Peyton Martin
#
# This script does the following:
#   - Packages frontend Lambda code
#   - Runs Terraform init if needed
#   - Creates ECR repository
#   - Builds Docker image
#   - Authenticates with ECR
#   - Pushes image to repository
#   - Deploys all AWS resources
#
# Requirements:
#   - AWS CLI configured
#   - Docker installed
#   - Terraform installed
################################

# Set variables
TERRAFORM_DIR="../terraform"
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
AWS_REGION=$(aws configure get region)
ECR_REPO="mathqs-lambda"
TAG="latest"

# Package Frontend Lambda packaging
echo "Building frontend Lambda..."
zip -j ../terraform/frontend/frontend_lambda.zip ../frontend/index.js ../frontend/index.html

# Initialize Terraform if needed
if [ ! -d "$TERRAFORM_DIR/.terraform" ]; then
    echo "Initializing Terraform..."
    (cd "$TERRAFORM_DIR" && terraform init)
fi

# Build ECR Repository 
echo "Creating ECR repository..."
(cd "$TERRAFORM_DIR" && terraform apply -target=aws_ecr_repository.mathqs_lambda -auto-approve)

# Build Docker image
echo "Building and pushing Docker image..."
docker build -t $ECR_REPO:$TAG ../lambda/

# Authenticate with ECR
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Tag image and push to ECR
docker tag $ECR_REPO:$TAG $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:$TAG
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:$TAG

# Deploy remaining infrastructure
echo "Deploying remaining infrastructure..."
(cd "$TERRAFORM_DIR" && terraform apply)