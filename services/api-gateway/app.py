from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import requests
import logging

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)

# Microservice URLs
FRAUD_SYSTEM_URL = os.getenv('FRAUD_SYSTEM_URL', 'http://localhost:8003')
PATTERN_ANALYZER_URL = os.getenv('PATTERN_ANALYZER_URL', 'http://localhost:8002')
DATA_COLLECTOR_URL = os.getenv('DATA_COLLECTOR_URL', 'http://localhost:8001')

@app.route('/api/health', methods=['GET'])
def health():
    # Check microservices health
    microservices_status = {}
    
    try:
        response = requests.get(f"{FRAUD_SYSTEM_URL}/health", timeout=5)
        microservices_status['fraud_system'] = 'healthy' if response.status_code == 200 else 'unhealthy'
    except:
        microservices_status['fraud_system'] = 'unavailable'
    
    return jsonify({
        "status": "healthy",
        "service": "api-gateway",
        "database": "connected" if os.getenv('DATABASE_URL') else "not configured",
        "microservices": microservices_status
    })

@app.route('/api/analyze-fraud', methods=['POST'])
def analyze_fraud():
    try:
        data = request.get_json()
        app.logger.info(f"Analyzing transaction: {data}")
        
        # Call fraud_system_v2 microservice
        try:
            fraud_response = requests.post(
                f"{FRAUD_SYSTEM_URL}/analyze-fraud",
                json=data,
                timeout=30
            )
            
            if fraud_response.status_code == 200:
                result = fraud_response.json()
                app.logger.info(f"Multi-agent analysis result: {result}")
                return jsonify(result)
            else:
                app.logger.error(f"Fraud system error: {fraud_response.status_code}")
                # Fallback to simple analysis
                return fallback_analysis(data)
                
        except requests.exceptions.RequestException as e:
            app.logger.error(f"Fraud system unavailable: {e}")
            # Fallback to simple analysis
            return fallback_analysis(data)
        
    except Exception as e:
        app.logger.error(f"Analysis error: {str(e)}")
        return jsonify({
            "error": "Analysis failed",
            "message": str(e),
            "is_fraud": False,
            "confidence_score": 0.0,
            "recommendation": "ERROR - Unable to analyze"
        }), 500

def fallback_analysis(data):
    """Fallback analysis when microservices are unavailable"""
    app.logger.info("Using fallback analysis")
    
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
    
    is_fraud = risk_score > 0.5
    confidence = min(risk_score, 1.0)
    
    if confidence > 0.8:
        recommendation = "BLOCK - High fraud risk detected"
    elif confidence > 0.5:
        recommendation = "REVIEW - Manual review recommended"
    else:
        recommendation = "APPROVE - Low fraud risk"
    
    return jsonify({
        "is_fraud": is_fraud,
        "confidence_score": confidence,
        "risk_factors": risk_factors,
        "recommendation": recommendation,
        "transaction_id": data.get('transaction_id'),
        "analysis_method": "fallback"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)