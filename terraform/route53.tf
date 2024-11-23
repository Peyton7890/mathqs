################################
# Route53 & ACM Configuration
# Purpose: Manages DNS and SSL certificate setup
#
# Components:
# 1. Route53
#    - Domain zone configuration
#    - A record for frontend
#
# 2. ACM (Certificate Manager)
#    - SSL certificate for domain
#    - DNS validation records
#    - Certificate validation
#
# Security:
# - TLS 1.2 for HTTPS
# - Automatic certificate renewal
################################

# Get existing Route53 zone
data "aws_route53_zone" "mathqs" {
  name         = "mathqs.com"
  private_zone = false
}

# ACM Certificate
resource "aws_acm_certificate" "mathqs" {
  domain_name       = "mathqs.com"
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}

# DNS validation records
resource "aws_route53_record" "cert_validation" {
  for_each = {
    for dvo in aws_acm_certificate.mathqs.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 60
  type            = each.value.type
  zone_id         = data.aws_route53_zone.mathqs.zone_id
}

# Certificate validation
resource "aws_acm_certificate_validation" "mathqs" {
  certificate_arn         = aws_acm_certificate.mathqs.arn
  validation_record_fqdns = [for record in aws_route53_record.cert_validation : record.fqdn]
}

# A record for the domain
resource "aws_route53_record" "frontend" {
  name    = "mathqs.com"
  type    = "A"
  zone_id = data.aws_route53_zone.mathqs.zone_id

  alias {
    name                   = aws_apigatewayv2_domain_name.frontend.domain_name_configuration[0].target_domain_name
    zone_id                = aws_apigatewayv2_domain_name.frontend.domain_name_configuration[0].hosted_zone_id
    evaluate_target_health = false
  }
}