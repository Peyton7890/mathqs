#!/bin/bash
# Author: Peyton Martin
# Description: Deployment script for MathQs application
# Steps:
#   1. Build frontend Lambda package
#   2. Build backend Lambda package
#   3. Create Python dependencies layer
#   4. Deploy infrastructure with Terraform

# Define paths
TERRAFORM_DIR="../terraform"
LAYER_DIR="../terraform/lambda/python"

## Build Lambdas ##
# Package frontend Lambda (HTML + JS)
echo "Building frontend Lambda..."
zip -j ../terraform/frontend/frontend_lambda.zip ../frontend/index.js ../frontend/index.html

# Package backend Lambda (Python)
echo "Building backend Lambda..."
zip -j ../terraform/lambda/lambda.zip ../lambda/*.py

## Create Lambda Layer ##
# Prepare directory for Python packages
mkdir -p $LAYER_DIR

# Set up Python virtual environment
python3.12 -m venv venv
source venv/bin/activate

# Install Python packages with manylinux compatibility
echo "Installing Python dependencies..."
pip install \
    --upgrade \
    -r ../lambda/requirements.txt \
    --platform manylinux2014_x86_64 \
    --implementation cp \
    --python-version 3.12 \
    --only-binary=:all: \
    --target $LAYER_DIR \
    --no-cache-dir

# Remove unnecessary files to reduce package size
echo "Cleaning up package files..."
find "$LAYER_DIR" -type d -name "tests" -exec rm -rf {} + 2>/dev/null
find "$LAYER_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find "$LAYER_DIR" -name "*.dist-info" -exec rm -rf {} +

# Create Lambda layer ZIP
echo "Creating Lambda layer..."
(cd $LAYER_DIR && zip -r ../lambda_layer.zip .)

# Clean up build artifacts
deactivate
rm -rf venv/
rm -rf $LAYER_DIR

## Deploy Infrastructure ##
# Initialize Terraform if needed
check_and_run_terraform_init() {
    if [ ! -d "$TERRAFORM_DIR/.terraform" ]; then
        echo "Initializing Terraform..."
        (cd "$TERRAFORM_DIR" && terraform init)
    fi
}

# Run Terraform deployment
check_and_run_terraform_init
echo "Planning Terraform changes..."
(cd "$TERRAFORM_DIR" && terraform plan)

echo "Applying Terraform changes..."
(cd "$TERRAFORM_DIR" && terraform apply)

# # Test TODO delete later ##
# Invoke the Lambda function
# echo "Invoking Lambda function..."
# aws lambda invoke --function-name mathqs_lambda --payload file://"test-event.json" response.json

# # Check if the response.json file was created and open it
# if [ -f "response.json" ]; then
#   echo "Opening response.json..."
#   if command -v xdg-open &> /dev/null; then
#     xdg-open response.json  # For Linux
#   elif command -v open &> /dev/null; then
#     open response.json       # For macOS
#   else
#     echo "Please open response.json manually. No suitable command found."
#   fi
# else
#   echo "response.json was not created. Check the Lambda function invocation."
# fi