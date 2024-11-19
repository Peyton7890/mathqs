# Author: Peyton Martin
# Description: Defines output values for the MathQs infrastructure
# Outputs:
#   - API Gateway endpoint URL for client applications
#   - Frontend URL for accessing the web interface

output "api_endpoint" {
  value = "${aws_apigatewayv2_stage.mathqs_stage.invoke_url}/generate"
  description = "API Gateway endpoint URL"
}

output "frontend_url" {
  value = "${aws_apigatewayv2_stage.frontend_stage.invoke_url}/generate"
  description = "Frontend application URL"
}