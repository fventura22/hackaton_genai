from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import random
import logging

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "service": "api-gateway",
        "database": "connected" if os.getenv('DATABASE_URL') else "not configured",
        "microservices": "standalone mode"
    })

@app.route('/api/analyze-fraud', methods=['POST'])
def analyze_fraud():
    try:
        data = request.get_json()
        app.logger.info(f"Analyzing transaction: {data}")
        
        # Simple fraud detection logic (standalone)
        amount = data.get('transaction_data', {}).get('amount', 0)
        location = data.get('transaction_data', {}).get('location', '')
        merchant = data.get('transaction_data', {}).get('merchant_category', '')
        
        # Basic fraud scoring
        risk_score = 0.0
        risk_factors = []
        
        if amount > 10000:
            risk_score += 0.4
            risk_factors.append("High transaction amount")
        elif amount > 5000:
            risk_score += 0.2
            risk_factors.append("Elevated transaction amount")
        
        if location.lower() in ['unknown', 'suspicious']:
            risk_score += 0.3
            risk_factors.append("Suspicious location")
        
        if merchant.lower() in ['online_gaming', 'crypto', 'gambling']:
            risk_score += 0.25
            risk_factors.append("High-risk merchant category")
        
        # Add some controlled randomness
        risk_score += random.uniform(0, 0.15)
        
        is_fraud = risk_score > 0.5
        confidence = min(risk_score, 1.0)
        
        if confidence > 0.8:
            recommendation = "BLOCK - High fraud risk detected"
        elif confidence > 0.5:
            recommendation = "REVIEW - Manual review recommended"
        else:
            recommendation = "APPROVE - Low fraud risk"
        
        result = {
            "is_fraud": is_fraud,
            "confidence_score": confidence,
            "risk_factors": risk_factors,
            "recommendation": recommendation,
            "transaction_id": data.get('transaction_id'),
            "analysis_method": "standalone"
        }
        
        app.logger.info(f"Analysis result: {result}")
        return jsonify(result)
        
    except Exception as e:
        app.logger.error(f"Analysis error: {str(e)}")
        return jsonify({
            "error": "Analysis failed",
            "message": str(e),
            "is_fraud": False,
            "confidence_score": 0.0,
            "recommendation": "ERROR - Unable to analyze"
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)