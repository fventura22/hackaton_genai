from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any
import numpy as np
from datetime import datetime, timedelta
import random

app = FastAPI(title="Pattern Analysis Service")

class PatternAnalysisRequest(BaseModel):
    transaction_data: Dict[str, Any]

class PatternAnalysisResponse(BaseModel):
    anomaly_score: float
    pattern_matches: list
    recent_transaction_count: int
    device_risk_score: float
    behavioral_analysis: Dict[str, Any]

class PatternAnalyzer:
    def __init__(self):
        # Known fraud patterns from fraud team analysis
        self.fraud_patterns = {
            "round_amounts": [100, 200, 500, 1000, 2000, 5000],
            "suspicious_sequences": ["multiple_small_then_large", "rapid_succession"],
            "high_risk_merchants": ["online_gaming", "crypto", "cash_advance"],
            "velocity_thresholds": {
                "transactions_per_hour": 5,
                "transactions_per_day": 20,
                "amount_per_hour": 5000
            }
        }
    
    def detect_amount_patterns(self, amount: float) -> tuple:
        """Detect suspicious amount patterns"""
        patterns = []
        score = 0.0
        
        # Check for round amounts (common in fraud)
        if amount in self.fraud_patterns["round_amounts"]:
            patterns.append(f"Round amount: ${amount}")
            score += 0.3
        
        # Check for amounts just under reporting thresholds
        reporting_thresholds = [3000, 5000, 10000]
        for threshold in reporting_thresholds:
            if threshold - 100 <= amount < threshold:
                patterns.append(f"Amount near reporting threshold: ${amount}")
                score += 0.5
        
        return score, patterns
    
    def analyze_transaction_velocity(self, transaction_data: Dict[str, Any]) -> tuple:
        """Analyze transaction velocity patterns"""
        # Simulate recent transaction analysis
        recent_count = random.randint(1, 10)
        patterns = []
        score = 0.0
        
        if recent_count > self.fraud_patterns["velocity_thresholds"]["transactions_per_hour"]:
            patterns.append(f"High velocity: {recent_count} transactions in last hour")
            score += 0.7
        
        return score, patterns, recent_count
    
    def analyze_merchant_risk(self, merchant_category: str) -> tuple:
        """Analyze merchant category risk"""
        patterns = []
        score = 0.0
        
        if merchant_category in self.fraud_patterns["high_risk_merchants"]:
            patterns.append(f"High-risk merchant category: {merchant_category}")
            score += 0.6
        
        return score, patterns
    
    def analyze_device_behavior(self, transaction_data: Dict[str, Any]) -> tuple:
        """Analyze device and behavioral patterns"""
        # Simulate device risk analysis
        device_risk = random.uniform(0, 1)
        patterns = []
        
        behavioral_analysis = {
            "typing_pattern_match": random.choice([True, False]),
            "mouse_movement_anomaly": random.choice([True, False]),
            "session_duration": random.randint(30, 3600),
            "ip_geolocation_mismatch": random.choice([True, False])
        }
        
        if device_risk > 0.7:
            patterns.append(f"High device risk score: {device_risk:.2f}")
        
        if behavioral_analysis["ip_geolocation_mismatch"]:
            patterns.append("IP geolocation mismatch detected")
            device_risk += 0.2
        
        return min(device_risk, 1.0), patterns, behavioral_analysis
    
    def detect_sequence_patterns(self, transaction_data: Dict[str, Any]) -> tuple:
        """Detect suspicious transaction sequences"""
        patterns = []
        score = 0.0
        
        # Simulate sequence analysis
        sequence_type = random.choice(["normal", "multiple_small_then_large", "rapid_succession"])
        
        if sequence_type in self.fraud_patterns["suspicious_sequences"]:
            patterns.append(f"Suspicious sequence detected: {sequence_type}")
            score += 0.5
        
        return score, patterns
    
    def calculate_anomaly_score(self, scores: list) -> float:
        """Calculate overall anomaly score"""
        if not scores:
            return 0.0
        
        # Use weighted average with emphasis on highest scores
        weights = np.exp(np.array(scores))
        weighted_score = np.average(scores, weights=weights)
        
        return min(weighted_score, 1.0)
    
    def analyze_patterns(self, request: PatternAnalysisRequest) -> PatternAnalysisResponse:
        """Main pattern analysis logic"""
        transaction = request.transaction_data
        all_patterns = []
        scores = []
        
        # Analyze different pattern types
        amount_score, amount_patterns = self.detect_amount_patterns(
            transaction.get("amount", 0)
        )
        scores.append(amount_score)
        all_patterns.extend(amount_patterns)
        
        velocity_score, velocity_patterns, recent_count = self.analyze_transaction_velocity(transaction)
        scores.append(velocity_score)
        all_patterns.extend(velocity_patterns)
        
        merchant_score, merchant_patterns = self.analyze_merchant_risk(
            transaction.get("merchant_category", "unknown")
        )
        scores.append(merchant_score)
        all_patterns.extend(merchant_patterns)
        
        device_risk, device_patterns, behavioral_analysis = self.analyze_device_behavior(transaction)
        scores.append(device_risk)
        all_patterns.extend(device_patterns)
        
        sequence_score, sequence_patterns = self.detect_sequence_patterns(transaction)
        scores.append(sequence_score)
        all_patterns.extend(sequence_patterns)
        
        # Calculate overall anomaly score
        anomaly_score = self.calculate_anomaly_score(scores)
        
        return PatternAnalysisResponse(
            anomaly_score=round(anomaly_score, 3),
            pattern_matches=all_patterns,
            recent_transaction_count=recent_count,
            device_risk_score=round(device_risk, 3),
            behavioral_analysis=behavioral_analysis
        )

analyzer = PatternAnalyzer()

@app.post("/analyze", response_model=PatternAnalysisResponse)
async def analyze_patterns(request: PatternAnalysisRequest):
    """Analyze transaction patterns for fraud indicators"""
    return analyzer.analyze_patterns(request)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "pattern-analyzer"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)