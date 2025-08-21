# Telco Fraud Detection System

A comprehensive fraud detection system built with microservices architecture, featuring AI-powered agents for automated fraud analysis and a React Native mobile application for fraud analysts.

## Architecture Overview

### Microservices
- **API Gateway** (Port 8000) - Central entry point and request orchestration
- **Fraud Detection Agent** (Port 8003) - Core AI agent for fraud decision making
- **Data Collection Service** (Port 8001) - Retrieves data from multiple sources
- **Pattern Analysis Service** (Port 8002) - Analyzes fraud patterns
- **User Management Service** (Port 8004) - Authentication and authorization
- **Notification Service** (Port 8005) - Alerts and notifications

### Infrastructure
- **PostgreSQL** - Primary database
- **Redis** - Caching and session management
- **RabbitMQ** - Message queue for inter-service communication

### Frontend
- **React Web Application** - Responsive web interface for fraud analysts (works on PC and mobile)

## Features

### AI-Powered Fraud Detection
- Multi-source data collection (customer profiles, transaction history, device info, external APIs)
- Pattern analysis based on fraud team insights
- Risk scoring with confidence levels
- Automated decision making with human oversight
- Real-time fraud alerts

### Web Application
- Responsive design (works on PC and mobile)
- Secure authentication
- Real-time dashboard with fraud statistics
- Interactive charts and visualizations
- Transaction analysis interface
- Detailed fraud investigation views
- Approve/Block/Review actions

### Fraud Detection Capabilities
- **Amount Analysis**: Detects unusual transaction amounts
- **Temporal Analysis**: Identifies suspicious timing patterns
- **Location Analysis**: Flags transactions from unusual locations
- **Velocity Analysis**: Detects rapid transaction sequences
- **Device Analysis**: Analyzes device fingerprints and behavior
- **Pattern Matching**: Identifies known fraud patterns

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 16+ (for mobile app development)
- Expo CLI (for React Native)

### 1. Start Backend Services
```bash
# Clone and navigate to project
cd hackaton-genai

# Start all services
docker-compose up -d

# Check service health
curl http://localhost:8000/api/health
```

### 2. Access Web Application
```bash
# Web app will be available at:
http://localhost:3000

# For development (optional):
cd services/web-frontend
npm install
npm start
```

### 3. Test the System
```bash
# Test fraud analysis endpoint
curl -X POST http://localhost:8000/api/analyze-fraud \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "CUST001",
    "transaction_id": "TXN123",
    "transaction_data": {
      "amount": 5000,
      "timestamp": "2024-01-15T02:30:00Z",
      "location": "Unknown",
      "merchant_category": "online_gaming"
    }
  }'
```

## Demo Credentials

### Web App Login
- **Fraud Analyst**: `fraud_analyst` / `analyst123`
- **Admin**: `admin` / `1234`

## API Documentation

### Main Endpoints

#### Analyze Fraud
```
POST /api/analyze-fraud
Content-Type: application/json

{
  "customer_id": "string",
  "transaction_id": "string", 
  "transaction_data": {
    "amount": number,
    "timestamp": "string",
    "location": "string",
    "merchant_category": "string"
  }
}
```

#### Response
```json
{
  "is_fraud": boolean,
  "confidence_score": number,
  "risk_factors": ["string"],
  "recommendation": "string"
}
```

## Fraud Detection Logic

### Risk Factors
1. **High Amount**: Transactions above $10,000 or 3x customer average
2. **Unusual Time**: Transactions during 12 AM - 6 AM
3. **Suspicious Location**: Unknown or high-risk locations
4. **High Velocity**: More than 5 transactions per hour
5. **Device Risk**: High device risk scores (>0.7)

### Decision Thresholds
- **Block** (>80%): High fraud risk - automatic block
- **Review** (50-80%): Medium risk - manual review required
- **Approve** (<50%): Low risk - allow transaction

## Monitoring and Alerts

### Real-time Monitoring
- Transaction volume and fraud rates
- System health and performance metrics
- Alert notifications via email/SMS

### Fraud Team Integration
- Pattern updates from fraud team analysis
- Configurable risk thresholds
- Historical fraud data analysis

## Deployment

### Production Deployment
1. Configure environment variables
2. Set up SSL certificates
3. Configure external data sources
4. Set up monitoring and logging
5. Deploy with Docker Compose or Kubernetes

### Environment Variables
```bash
DATABASE_URL=postgresql://user:pass@host:5432/db
REDIS_URL=redis://host:6379
RABBITMQ_URL=amqp://user:pass@host:5672
JWT_SECRET=your-secret-key
```

## Security Features

- JWT-based authentication
- Role-based access control
- Encrypted data transmission
- Secure API endpoints
- Input validation and sanitization

## Contributing

1. Fork the repository
2. Create feature branch
3. Implement changes with tests
4. Submit pull request

## License

This project is licensed under the MIT License.

## Support

For technical support or questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation wiki