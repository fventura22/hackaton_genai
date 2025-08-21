# ECR Repositories
resource "aws_ecr_repository" "api_gateway" {
  name                 = "${var.project_name}-api-gateway"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name = "${var.project_name}-api-gateway"
  }
}

resource "aws_ecr_repository" "web_frontend" {
  name                 = "${var.project_name}-web-frontend"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name = "${var.project_name}-web-frontend"
  }
}

resource "aws_ecr_repository" "fraud_agent" {
  name                 = "${var.project_name}-fraud-agent"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name = "${var.project_name}-fraud-agent"
  }
}

resource "aws_ecr_repository" "data_collector" {
  name                 = "${var.project_name}-data-collector"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name = "${var.project_name}-data-collector"
  }
}

resource "aws_ecr_repository" "pattern_analyzer" {
  name                 = "${var.project_name}-pattern-analyzer"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name = "${var.project_name}-pattern-analyzer"
  }
}

resource "aws_ecr_repository" "user_service" {
  name                 = "${var.project_name}-user-service"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name = "${var.project_name}-user-service"
  }
}

resource "aws_ecr_repository" "notification_service" {
  name                 = "${var.project_name}-notification-service"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name = "${var.project_name}-notification-service"
  }
}