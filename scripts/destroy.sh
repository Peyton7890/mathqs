#!/bin/bash
# Author: Peyton Martin
# Description: Cleanup script for MathQs application
# Actions:
#   1. Destroy all AWS infrastructure
#   2. Clean up local build artifacts

# Set Terraform directory path
TERRAFORM_DIR="../terraform"

# Destroy AWS infrastructure
echo "Destroying AWS infrastructure..."
(cd "$TERRAFORM_DIR" && terraform destroy -auto-approve)

# Clean up local files
echo "Cleaning up local files..."
rm -f "response.json"
rm -f "../terraform/lambda/lambda.zip"
rm -f "../terraform/lambda/lambda_layer.zip"
rm -f "../terraform/frontend/frontend_lambda.zip"

echo "Cleanup complete!"

