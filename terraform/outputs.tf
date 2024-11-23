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
  value = "https://mathqs.com"
  description = "Frontend application URL"
}

output "nameservers" {
  value       = data.aws_route53_zone.mathqs.name_servers
  description = "Nameservers for domain configuration"
}

output "domain_status" {
  value = "Domain configuration is complete. The website will be available at https://mathqs.com once DNS propagates (usually 15-30 minutes)"
  description = "Domain setup status"
}

output "domain_nameservers" {
  value = data.aws_route53_zone.mathqs.name_servers
  description = "Domain nameservers (these are automatically configured by Route53)"
}