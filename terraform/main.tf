################################
# Main Configuration
# Purpose: Defines core AWS provider settings
#
# Components:
# - AWS Provider configuration with region settings
################################

provider "aws" {
  region = "us-east-1"
}

data "aws_region" "current" {}