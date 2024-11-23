################################
# API Gateway Configuration
# Purpose: Manages HTTP endpoints for the application
#
# Components:
# 1. Backend API Gateway
#    - Handles PDF generation requests
#    - CORS enabled for web access
#    - POST /generate endpoint
#
# 2. Frontend API Gateway
#    - Serves web interface
#    - GET /generate endpoint
#
# Security:
# - Lambda permissions for API Gateway invocation
# - CORS policies for frontend access
################################

## Backend API Gateway resources ##

# Create the HTTP API Gateway
resource "aws_apigatewayv2_api" "mathqs_api" {
  name          = "mathqs-api"
  protocol_type = "HTTP"
  cors_configuration {
    allow_origins = ["*"]
    allow_methods = ["POST"]
    allow_headers = ["content-type"]
    max_age      = 300
  }
}

resource "aws_apigatewayv2_stage" "mathqs_stage" {
  api_id = aws_apigatewayv2_api.mathqs_api.id
  name   = "prod"
  auto_deploy = true
}

resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id           = aws_apigatewayv2_api.mathqs_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.mathqs_lambda.invoke_arn
  integration_method = "POST"
}

resource "aws_apigatewayv2_route" "lambda_route" {
  api_id    = aws_apigatewayv2_api.mathqs_api.id
  route_key = "POST /generate"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

resource "aws_lambda_permission" "api_gw" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.mathqs_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.mathqs_api.execution_arn}/*/*"
}

## Frontend API Gateway resources ##

# Frontend API Gateway
resource "aws_apigatewayv2_api" "frontend_api" {
  name          = "mathqs-frontend-api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_stage" "frontend_stage" {
  api_id = aws_apigatewayv2_api.frontend_api.id
  name   = "prod"
  auto_deploy = true
}

resource "aws_apigatewayv2_integration" "frontend_lambda_integration" {
  api_id           = aws_apigatewayv2_api.frontend_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.frontend_lambda.invoke_arn
  integration_method = "POST"
}

resource "aws_apigatewayv2_route" "frontend_route" {
  api_id    = aws_apigatewayv2_api.frontend_api.id
  route_key = "GET /"  # Changed from "GET /generate"
  target    = "integrations/${aws_apigatewayv2_integration.frontend_lambda_integration.id}"
}

resource "aws_lambda_permission" "frontend_api_gw" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.frontend_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.frontend_api.execution_arn}/*/*"
}

# Custom domain configuration for frontend
resource "aws_apigatewayv2_domain_name" "frontend" {
  domain_name = "mathqs.com"
  domain_name_configuration {
    certificate_arn = aws_acm_certificate.mathqs.arn
    endpoint_type   = "REGIONAL"
    security_policy = "TLS_1_2"
  }
  depends_on = [aws_acm_certificate_validation.mathqs]
}

resource "aws_apigatewayv2_api_mapping" "frontend" {
  api_id      = aws_apigatewayv2_api.frontend_api.id
  domain_name = aws_apigatewayv2_domain_name.frontend.id
  stage       = aws_apigatewayv2_stage.frontend_stage.id
}