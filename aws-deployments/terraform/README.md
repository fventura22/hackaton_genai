# Fraud Detection System - Terraform Infrastructure

Complete Terraform infrastructure for the fraud detection system with ECS Fargate, Cognito authentication, and supporting services.

## 🏗️ **Infrastructure Components**

### **Networking**
- VPC with public and private subnets across 2 AZs
- Internet Gateway and NAT Gateways
- Route tables and security groups

### **Compute**
- ECS Fargate cluster with all microservices
- Application Load Balancer with Cognito authentication
- Auto-scaling and health checks

### **Storage & Cache**
- RDS PostgreSQL database
- ElastiCache Redis cluster
- ECR repositories for container images

### **Authentication**
- Cognito User Pool with admin/analyst groups
- Demo users with secure passwords
- OAuth2 integration with ALB

## 🚀 **Quick Start**

### **1. Prerequisites**
```bash
# Install Terraform
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update && sudo apt-get install terraform

# Configure AWS credentials
aws configure
```

### **2. Deploy Infrastructure**
```bash
cd aws-deployments/terraform

# Copy and customize variables
cp terraform.tfvars.example terraform.tfvars

# Initialize Terraform
terraform init

# Plan deployment
terraform plan

# Deploy infrastructure
terraform apply
```

### **3. Build and Push Images**
```bash
# Get ECR login
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Build and push each service
docker build -t fraud-detection-tf-api-gateway ../../services/api-gateway
docker tag fraud-detection-tf-api-gateway:latest ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/fraud-detection-tf-api-gateway:latest
docker push ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/fraud-detection-tf-api-gateway:latest

# Repeat for all services...
```

### **4. Update ECS Service**
```bash
# Force new deployment after pushing images
aws ecs update-service --cluster fraud-detection-tf-cluster --service fraud-detection-tf-service --force-new-deployment
```

## 📋 **Resource Naming Convention**

All resources use the pattern: `{project_name}-{resource_type}`

Examples:
- VPC: `fraud-detection-tf-vpc`
- ECS Cluster: `fraud-detection-tf-cluster`
- ALB: `fraud-detection-tf-alb`
- RDS: `fraud-detection-tf-postgres`

## 🔐 **Security Features**

### **Network Security**
- Private subnets for ECS tasks and databases
- Security groups with least privilege access
- NAT Gateways for outbound internet access

### **Authentication**
- Cognito User Pool with strong password policies
- ALB-integrated OAuth2 authentication
- Role-based access (admin/analyst groups)

### **Data Protection**
- RDS encryption at rest
- ECR image scanning enabled
- CloudWatch logs for monitoring

## 🎯 **Demo Users**

After deployment, use these credentials:

- **Admin:** admin@frauddetection.com / Admin123!
- **Analyst:** analyst@frauddetection.com / Analyst123!

## 📊 **Outputs**

Terraform provides these important outputs:

```bash
# Get ALB URL
terraform output alb_url

# Get Cognito configuration
terraform output cognito_user_pool_id
terraform output cognito_client_id
terraform output cognito_domain

# Get ECR repositories
terraform output ecr_repositories
```

## 🔧 **Customization**

### **Variables**
Edit `terraform.tfvars` to customize:
- AWS region
- VPC CIDR blocks
- ECS task resources
- Project naming

### **Scaling**
Adjust in `variables.tf`:
- `desired_count` - Number of ECS tasks
- `container_cpu` - CPU units per task
- `container_memory` - Memory per task

## 🧹 **Cleanup**

```bash
# Destroy all resources
terraform destroy

# Confirm with 'yes'
```

## 📁 **File Structure**

```
terraform/
├── main.tf              # Provider and data sources
├── variables.tf         # Input variables
├── vpc.tf              # VPC and networking
├── security_groups.tf  # Security groups
├── cognito.tf          # Cognito User Pool
├── alb.tf              # Application Load Balancer
├── ecs.tf              # ECS cluster and services
├── rds.tf              # PostgreSQL database
├── elasticache.tf      # Redis cache
├── ecr.tf              # Container repositories
├── outputs.tf          # Output values
└── README.md           # This file
```

## 🔍 **Troubleshooting**

### **Common Issues**

1. **ECR Images Not Found**
   - Build and push images to ECR repositories first
   - Check repository URLs in outputs

2. **ECS Tasks Failing**
   - Check CloudWatch logs: `/ecs/fraud-detection-tf`
   - Verify security group rules

3. **ALB Health Checks Failing**
   - Ensure containers are listening on correct ports
   - Check target group health in AWS Console

4. **Cognito Authentication Issues**
   - Verify callback URLs match ALB DNS name
   - Check user pool domain configuration

### **Useful Commands**

```bash
# Check ECS service status
aws ecs describe-services --cluster fraud-detection-tf-cluster --services fraud-detection-tf-service

# View ECS logs
aws logs tail /ecs/fraud-detection-tf --follow

# Check ALB target health
aws elbv2 describe-target-health --target-group-arn TARGET_GROUP_ARN
```

## 🎉 **Success!**

After successful deployment:

1. **Access your application** at the ALB URL
2. **Login with demo credentials**
3. **Explore the fraud detection dashboard**

Your enterprise-grade fraud detection system is now running on AWS! 🚀