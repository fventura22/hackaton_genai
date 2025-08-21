# Cognito User Pool
resource "aws_cognito_user_pool" "main" {
  name = "${var.project_name}-users"

  password_policy {
    minimum_length    = 8
    require_lowercase = true
    require_numbers   = true
    require_symbols   = false
    require_uppercase = true
  }

  auto_verified_attributes = ["email"]
  username_attributes      = ["email"]

  tags = {
    Name = "${var.project_name}-user-pool"
  }
}

# Cognito User Pool Client
resource "aws_cognito_user_pool_client" "main" {
  name         = "${var.project_name}-client"
  user_pool_id = aws_cognito_user_pool.main.id

  generate_secret                      = true
  explicit_auth_flows                  = ["ADMIN_NO_SRP_AUTH", "USER_PASSWORD_AUTH"]
  allowed_oauth_flows_user_pool_client = true
  allowed_oauth_flows                  = ["code"]
  allowed_oauth_scopes                 = ["openid", "email", "profile"]
  supported_identity_providers         = ["COGNITO"]

  # callback_urls = [
  #   "https://${aws_lb.main.dns_name}/oauth2/idpresponse"
  # ]

  # logout_urls = [
  #   "https://${aws_lb.main.dns_name}/"
  # ]
}

# Cognito User Pool Domain
resource "aws_cognito_user_pool_domain" "main" {
  domain       = "${var.project_name}-${random_id.cognito_domain.hex}"
  user_pool_id = aws_cognito_user_pool.main.id
}

resource "random_id" "cognito_domain" {
  byte_length = 4
}

# Admin Group
resource "aws_cognito_user_group" "admin" {
  name         = "admin"
  user_pool_id = aws_cognito_user_pool.main.id
  description  = "Administrator users with full access"
}

# Analyst Group
resource "aws_cognito_user_group" "analyst" {
  name         = "analyst"
  user_pool_id = aws_cognito_user_pool.main.id
  description  = "Fraud analyst users with limited access"
}

# Demo Admin User
resource "aws_cognito_user" "admin" {
  user_pool_id = aws_cognito_user_pool.main.id
  username     = "admin@frauddetection.com"

  attributes = {
    email          = "admin@frauddetection.com"
    email_verified = true
  }

  password = "Admin123!"

  lifecycle {
    ignore_changes = [password]
  }
}

# Demo Analyst User
resource "aws_cognito_user" "analyst" {
  user_pool_id = aws_cognito_user_pool.main.id
  username     = "analyst@frauddetection.com"

  attributes = {
    email          = "analyst@frauddetection.com"
    email_verified = true
  }

  password = "Analyst123!"

  lifecycle {
    ignore_changes = [password]
  }
}

# Add users to groups
resource "aws_cognito_user_in_group" "admin" {
  user_pool_id = aws_cognito_user_pool.main.id
  group_name   = aws_cognito_user_group.admin.name
  username     = aws_cognito_user.admin.username
}

resource "aws_cognito_user_in_group" "analyst" {
  user_pool_id = aws_cognito_user_pool.main.id
  group_name   = aws_cognito_user_group.analyst.name
  username     = aws_cognito_user.analyst.username
}