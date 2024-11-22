################################
# Output Definitions
# Purpose: Provides essential URLs and endpoints
#
# Outputs:
# - api_endpoint: Backend API URL for PDF generation
# - frontend_url: User interface access point
#
# Usage: Values are displayed after terraform apply
################################

output "api_endpoint" {
  value = "${aws_apigatewayv2_stage.mathqs_stage.invoke_url}/generate"
  description = "API Gateway endpoint URL"
}

output "frontend_url" {
  value = "${aws_apigatewayv2_stage.frontend_stage.invoke_url}/generate"
  description = "Frontend application URL"
}