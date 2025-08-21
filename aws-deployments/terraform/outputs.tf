output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "alb_dns_name" {
  description = "DNS name of the load balancer"
  value       = aws_lb.main.dns_name
}

output "alb_url" {
  description = "HTTPS URL of the load balancer"
  value       = "https://${aws_lb.main.dns_name}"
}

output "alb_http_url" {
  description = "HTTP URL (redirects to HTTPS)"
  value       = "http://${aws_lb.main.dns_name}"
}

output "cognito_user_pool_id" {
  description = "ID of the Cognito User Pool"
  value       = aws_cognito_user_pool.main.id
}

output "cognito_client_id" {
  description = "ID of the Cognito User Pool Client"
  value       = aws_cognito_user_pool_client.main.id
}

output "cognito_domain" {
  description = "Cognito User Pool Domain"
  value       = "${aws_cognito_user_pool_domain.main.domain}.auth.${var.aws_region}.amazoncognito.com"
}

output "rds_endpoint" {
  description = "RDS instance endpoint"
  value       = aws_db_instance.main.endpoint
  sensitive   = true
}



output "ecs_cluster_name" {
  description = "Name of the ECS cluster"
  value       = aws_ecs_cluster.main.name
}

output "ecr_repositories" {
  description = "ECR repository URLs"
  value = {
    api_gateway         = aws_ecr_repository.api_gateway.repository_url
    web_frontend        = aws_ecr_repository.web_frontend.repository_url
    fraud_agent         = aws_ecr_repository.fraud_agent.repository_url
    user_service        = aws_ecr_repository.user_service.repository_url
    data_collector      = aws_ecr_repository.data_collector.repository_url
    pattern_analyzer    = aws_ecr_repository.pattern_analyzer.repository_url
    notification_service = aws_ecr_repository.notification_service.repository_url
    fraud_system_v2     = aws_ecr_repository.fraud_system_v2.repository_url
  }
}

output "demo_users" {
  description = "Demo user credentials"
  value = {
    admin = {
      username = aws_cognito_user.admin.username
      password = "Admin123!"
    }
    analyst = {
      username = aws_cognito_user.analyst.username
      password = "Analyst123!"
    }
  }
}