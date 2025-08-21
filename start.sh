#!/bin/bash

echo "🚀 Starting Telco Fraud Detection System..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Build and start services
echo "📦 Building and starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 30

# Check service health
echo "🔍 Checking service health..."

services=("api-gateway:8000" "data-collector:8001" "pattern-analyzer:8002" "fraud-agent:8003" "user-service:8004" "notification-service:8005")

for service in "${services[@]}"; do
    name=$(echo $service | cut -d: -f1)
    port=$(echo $service | cut -d: -f2)
    
    if curl -s http://localhost:$port/health > /dev/null; then
        echo "✅ $name is healthy"
    else
        echo "❌ $name is not responding"
    fi
done

echo ""
echo "🎉 System is ready!"
echo ""
echo "🌐 Web App:"
echo "   Frontend: http://localhost:3000"
echo "   Login with demo credentials below"
echo ""
echo "🔗 API Endpoints:"
echo "   API Gateway: http://localhost:8000"
echo "   Health Check: http://localhost:8000/api/health"
echo ""
echo "🧪 Test Fraud Analysis:"
echo "   curl -X POST http://localhost:8000/api/analyze-fraud \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"customer_id\":\"CUST001\",\"transaction_id\":\"TXN123\",\"transaction_data\":{\"amount\":5000,\"timestamp\":\"2024-01-15T02:30:00Z\",\"location\":\"Unknown\",\"merchant_category\":\"online_gaming\"}}'"
echo ""
echo "👤 Demo Credentials:"
echo "   Fraud Analyst: fraud_analyst / analyst123"
echo "   Admin: admin / 1234"