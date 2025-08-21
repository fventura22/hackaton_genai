from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any, List
import numpy as np
from datetime import datetime
import json

app = FastAPI(title="Fraud Detection Agent")

class FraudDecisionRequest(BaseModel):
    customer_data: Dict[str, Any]
    pattern_analysis: Dict[str, Any]
    transaction_data: Dict[str, Any]

class FraudDecisionResponse(BaseModel):
    is_fraud: bool
    confidence_score: float
    risk_factors: List[str]
    recommendation: str

class FraudDetectionAgent:
    def __init__(self):
        # Fraud patterns learned from fraud team
        self.fraud_patterns = {
            "high_amount_threshold": 10000,
            "unusual_time_hours": [0, 1, 2, 3, 4, 5],
            "suspicious_locations": ["unknown", "high_risk"],
            "velocity_threshold": 5,  # transactions per hour
            "device_risk_score_threshold": 0.7
        }
        
        self.risk_weights = {
            "amount": 0.25,
            "time": 0.15,
            "location": 0.20,
            "velocity": 0.20,
            "device": 0.20
        }
    
    def analyze_transaction_amount(self, amount: float, customer_avg: float) -> tuple:
        """Analyze transaction amount risk"""
        risk_score = 0.0
        factors = []
        
        if amount > self.fraud_patterns["high_amount_threshold"]:
            risk_score += 0.8
            factors.append(f"High amount: ${amount}")
        
        if customer_avg > 0 and amount > customer_avg * 3:
            risk_score += 0.6
            factors.append(f"Amount 3x higher than average: ${amount} vs ${customer_avg}")
        
        return min(risk_score, 1.0), factors
    
    def analyze_transaction_time(self, timestamp: str) -> tuple:
        """Analyze transaction timing risk"""
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            hour = dt.hour
            
            if hour in self.fraud_patterns["unusual_time_hours"]:
                return 0.7, [f"Unusual time: {hour}:00"]
        except:
            pass
        
        return 0.0, []
    
    def analyze_location_risk(self, location: str, customer_locations: List[str]) -> tuple:
        """Analyze location-based risk"""
        risk_score = 0.0
        factors = []
        
        if location in self.fraud_patterns["suspicious_locations"]:
            risk_score += 0.9
            factors.append(f"Suspicious location: {location}")
        
        if location not in customer_locations:
            risk_score += 0.5
            factors.append(f"New location: {location}")
        
        return min(risk_score, 1.0), factors
    
    def analyze_velocity(self, recent_transactions: int) -> tuple:
        """Analyze transaction velocity"""
        if recent_transactions > self.fraud_patterns["velocity_threshold"]:
            return 0.8, [f"High velocity: {recent_transactions} transactions/hour"]
        return 0.0, []
    
    def analyze_device_risk(self, device_score: float) -> tuple:
        """Analyze device risk score"""
        if device_score > self.fraud_patterns["device_risk_score_threshold"]:
            return device_score, [f"High device risk score: {device_score}"]
        return 0.0, []
    
    def make_decision(self, request: FraudDecisionRequest) -> FraudDecisionResponse:
        """Main decision-making logic"""
        risk_factors = []
        risk_scores = {}
        
        # Extract data
        transaction = request.transaction_data
        customer = request.customer_data.get("customer_profile", {})
        patterns = request.pattern_analysis
        
        # Analyze different risk dimensions
        amount_risk, amount_factors = self.analyze_transaction_amount(
            transaction.get("amount", 0),
            customer.get("avg_transaction_amount", 0)
        )
        risk_scores["amount"] = amount_risk
        risk_factors.extend(amount_factors)
        
        time_risk, time_factors = self.analyze_transaction_time(
            transaction.get("timestamp", "")
        )
        risk_scores["time"] = time_risk
        risk_factors.extend(time_factors)
        
        location_risk, location_factors = self.analyze_location_risk(
            transaction.get("location", ""),
            customer.get("frequent_locations", [])
        )
        risk_scores["location"] = location_risk
        risk_factors.extend(location_factors)
        
        velocity_risk, velocity_factors = self.analyze_velocity(
            patterns.get("recent_transaction_count", 0)
        )
        risk_scores["velocity"] = velocity_risk
        risk_factors.extend(velocity_factors)
        
        device_risk, device_factors = self.analyze_device_risk(
            patterns.get("device_risk_score", 0)
        )
        risk_scores["device"] = device_risk
        risk_factors.extend(device_factors)
        
        # Calculate weighted confidence score
        confidence_score = sum(
            risk_scores[factor] * self.risk_weights[factor]
            for factor in risk_scores
        )
        
        # Make final decision
        is_fraud = confidence_score > 0.5
        
        # Generate recommendation
        if confidence_score > 0.8:
            recommendation = "BLOCK - High fraud risk detected"
        elif confidence_score > 0.5:
            recommendation = "REVIEW - Manual review required"
        else:
            recommendation = "APPROVE - Low fraud risk"
        
        return FraudDecisionResponse(
            is_fraud=is_fraud,
            confidence_score=round(confidence_score, 3),
            risk_factors=risk_factors,
            recommendation=recommendation
        )

agent = FraudDetectionAgent()

@app.post("/decide", response_model=FraudDecisionResponse)
async def make_fraud_decision(request: FraudDecisionRequest):
    """Make fraud detection decision based on collected data and patterns"""
    return agent.make_decision(request)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "fraud-agent"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)