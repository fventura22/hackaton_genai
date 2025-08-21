#!/bin/bash

# ECS Fargate Deployment Script
echo "🚀 Deploying Fraud Detection System to ECS Fargate..."

# Variables
CLUSTER_NAME="fraud-detection-cluster"
SERVICE_NAME="fraud-detection-service"
REGION="us-east-1"

# Create ECR repositories
aws ecr create-repository --repository-name fraud-detection-api-gateway --region $REGION
aws ecr create-repository --repository-name fraud-detection-fraud-agent --region $REGION
aws ecr create-repository --repository-name fraud-detection-data-collector --region $REGION
aws ecr create-repository --repository-name fraud-detection-pattern-analyzer --region $REGION
aws ecr create-repository --repository-name fraud-detection-user-service --region $REGION
aws ecr create-repository --repository-name fraud-detection-notification-service --region $REGION

# Build and push images
docker build -t fraud-detection-api-gateway ../../services/api-gateway
docker build -t fraud-detection-fraud-agent ../../services/fraud-agent
docker build -t fraud-detection-data-collector ../../services/data-collector
docker build -t fraud-detection-pattern-analyzer ../../services/pattern-analyzer
docker build -t fraud-detection-user-service ../../services/user-service
docker build -t fraud-detection-notification-service ../../services/notification-service

# Create ECS cluster
aws ecs create-cluster --cluster-name $CLUSTER_NAME --region $REGION

# Register task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json --region $REGION

# Create service
aws ecs create-service \
  --cluster $CLUSTER_NAME \
  --service-name $SERVICE_NAME \
  --task-definition fraud-detection-system \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx,subnet-yyy],securityGroups=[sg-xxx],assignPublicIp=ENABLED}" \
  --region $REGION

echo "✅ ECS Fargate deployment initiated!"