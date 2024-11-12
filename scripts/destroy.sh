#!/bin/bash

# Path to the Terraform directory and response file
TERRAFORM_DIR="../terraform"

# Run Terraform destroy with auto-approve
echo "Running 'terraform destroy'..."
(cd "$TERRAFORM_DIR" && terraform destroy -auto-approve)

# Remove response.json and lambda.zip
rm "response.json"
rm "../terraform/lambda.zip"
