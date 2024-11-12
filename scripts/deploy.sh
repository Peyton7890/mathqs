#!/bin/bash

# Paths to Terraform and script directories
TERRAFORM_DIR="../terraform"

# Define function to check if terraform init has been run
check_and_run_terraform_init() {
  if [ ! -d "$TERRAFORM_DIR/.terraform" ]; then
    echo "Terraform has not been initialized. Running 'terraform init'..."
    (cd "$TERRAFORM_DIR" && terraform init)
  else
    echo "Terraform is already initialized."
  fi
}

# Zip .py files from the lambda folder
echo "Zipping .py files from ../lambda to ../terraform/lambda.zip..."
zip -j ../terraform/lambda/lambda.zip ../lambda/*.py

# Run Terraform init if needed
check_and_run_terraform_init

# Run Terraform plan
echo "Running 'terraform plan'..."
(cd "$TERRAFORM_DIR" && terraform plan)

# Apply Terraform changes
echo "Running 'terraform apply'..."
(cd "$TERRAFORM_DIR" && terraform apply)

# Invoke the Lambda function
echo "Invoking Lambda function..."
aws lambda invoke --function-name my_lambda_function --payload file://"test-event.json" response.json

# Check if the response.json file was created and open it
if [ -f "response.json" ]; then
  echo "Opening response.json..."
  if command -v xdg-open &> /dev/null; then
    xdg-open response.json  # For Linux
  elif command -v open &> /dev/null; then
    open response.json       # For macOS
  else
    echo "Please open response.json manually. No suitable command found."
  fi
else
  echo "response.json was not created. Check the Lambda function invocation."
fi
