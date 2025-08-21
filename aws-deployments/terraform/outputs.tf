output "alb_url" {
  description = "URL of the Application Load Balancer"
  value       = "http://${aws_lb.main.dns_name}"
}

output "alb_dns_name" {
  description = "DNS name of the Application Load Balancer"
  value       = aws_lb.main.dns_name
}

output "ecs_cluster_name" {
  description = "Name of the ECS cluster"
  value       = aws_ecs_cluster.main.name
}

output "ecs_service_name" {
  description = "Name of the ECS service"
  value       = aws_ecs_service.main.name
}

output "rds_endpoint" {
  description = "RDS instance endpoint"
  value       = aws_db_instance.main.endpoint
  sensitive   = true
}

output "ecr_repositories" {
  description = "ECR repository URLs"
  value = {
    api_gateway         = aws_ecr_repository.api_gateway.repository_url
    web_frontend        = aws_ecr_repository.web_frontend.repository_url
    fraud_agent         = aws_ecr_repository.fraud_agent.repository_url
    data_collector      = aws_ecr_repository.data_collector.repository_url
    pattern_analyzer    = aws_ecr_repository.pattern_analyzer.repository_url
    user_service        = aws_ecr_repository.user_service.repository_url
    notification_service = aws_ecr_repository.notification_service.repository_url
  }
}

output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "IDs of the public subnets"
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "IDs of the private subnets"
  value       = aws_subnet.private[*].id
}