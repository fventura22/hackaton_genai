#!/bin/bash

echo "🚀 Starting Telco Fraud Detection System for Network Access..."

# Get local IP address
LOCAL_IP=$(hostname -I | awk '{print $1}')

echo "🌐 Your local IP address: $LOCAL_IP"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Build and start services
echo "📦 Building and starting services..."
docker-compose down
docker-compose up -d --build

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
echo "🎉 System is ready for network access!"
echo ""
echo "🌐 Access from any device on your network:"
echo "   Local PC: http://localhost:3000"
echo "   Other devices: http://$LOCAL_IP:3000"
echo ""
echo "🔗 API Endpoints:"
echo "   Local: http://localhost:8000/api/health"
echo "   Network: http://$LOCAL_IP:8000/api/health"
echo ""
echo "👤 Demo Credentials:"
echo "   Fraud Analyst: fraud_analyst / analyst123"
echo "   Admin: admin / 1234"
echo ""
echo "📱 Mobile Access:"
echo "   Open http://$LOCAL_IP:3000 on your phone/tablet"