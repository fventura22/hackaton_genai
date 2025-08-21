#!/bin/bash

echo "🧪 Testing Fraud Detection API..."

# Test 1: High Risk Transaction
echo "Test 1: High Risk Transaction (Large amount, unusual time, suspicious location)"
curl -X POST http://localhost:8000/api/analyze-fraud \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "CUST001",
    "transaction_id": "TXN001",
    "transaction_data": {
      "amount": 15000,
      "timestamp": "2024-01-15T02:30:00Z",
      "location": "Unknown",
      "merchant_category": "online_gaming"
    }
  }' | jq '.'

echo -e "\n" && sleep 2

# Test 2: Medium Risk Transaction  
echo "Test 2: Medium Risk Transaction (Moderate amount, normal time)"
curl -X POST http://localhost:8000/api/analyze-fraud \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "CUST002",
    "transaction_id": "TXN002", 
    "transaction_data": {
      "amount": 800,
      "timestamp": "2024-01-15T14:30:00Z",
      "location": "New York",
      "merchant_category": "retail"
    }
  }' | jq '.'

echo -e "\n" && sleep 2

# Test 3: Low Risk Transaction
echo "Test 3: Low Risk Transaction (Small amount, normal patterns)"
curl -X POST http://localhost:8000/api/analyze-fraud \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "CUST001",
    "transaction_id": "TXN003",
    "transaction_data": {
      "amount": 50,
      "timestamp": "2024-01-15T12:00:00Z", 
      "location": "Boston",
      "merchant_category": "grocery"
    }
  }' | jq '.'

echo -e "\n" && sleep 2

# Test 4: Authentication Test
echo "Test 4: User Authentication"
curl -X POST http://localhost:8004/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "fraud_analyst",
    "password": "analyst123"
  }' | jq '.'

echo -e "\n"
echo "✅ API Testing Complete!"