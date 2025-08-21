#!/usr/bin/env python3
"""FastAPI wrapper for fraud_system_v2 multi-agent system"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.agente_master import agente_master

app = FastAPI(title="Fraud Detection Multi-Agent System v2")

class FraudAnalysisRequest(BaseModel):
    customer_id: str
    transaction_id: str
    transaction_data: Dict[str, Any]

class FraudAnalysisResponse(BaseModel):
    is_fraud: bool
    confidence_score: float
    risk_factors: List[str]
    recommendation: str
    decision: str
    analysis_method: str = "multi-agent-v2"

class FraudSystemV2:
    def __init__(self):
        """Initialize the multi-agent system"""
        print("🚀 Starting FraudSystemV2 initialization...")
        try:
            print("🔗 Creating master agent...")
            self.master_agent = agente_master()
            print("✅ Multi-agent system ready")
        except Exception as e:
            print(f"❌ Failed to initialize master agent: {e}")
            print(f"🔍 Error type: {type(e).__name__}")
            import traceback
            print(f"📋 Full stack trace:")
            traceback.print_exc()
            self.master_agent = None
            print("⚠️ System will operate in degraded mode")
    
    def analyze_transaction(self, request: FraudAnalysisRequest) -> FraudAnalysisResponse:
        """Analyze transaction using multi-agent system"""
        if not self.master_agent:
            raise HTTPException(status_code=500, detail="Multi-agent system not initialized")
        
        try:
            # Extract transaction data
            customer_id = request.customer_id
            amount = request.transaction_data.get('amount', 0)
            
            # Use multi-agent analysis
            result = self.master_agent.analizar_transaccion(
                numero_documento=customer_id,
                importe=float(amount)
            )
            
            # Convert to API response format
            is_fraud = result['decision'] in ['BLOQUEAR', 'REVISAR']
            confidence_score = result['probabilidad_final']
            
            # Extract risk factors with weights and contributions
            risk_factors = []
            weights = result.get('pesos_utilizados', {})
            
            for agent_name, analysis in result['analisis_detallado'].items():
                prob = analysis.get('probabilidad_fraude', 0)
                reason = analysis.get('razon', f'{agent_name} analysis')
                weight = weights.get(agent_name, 0)
                contribution = prob * weight
                
                # Show all agents with their weights and contributions
                if prob > 0 or weight > 0:
                    risk_factors.append(
                        f"{agent_name.capitalize()}: {reason} "
                        f"[Risk: {prob:.1%}, Weight: {weight:.1%}, Contribution: {contribution:.1%}]"
                    )
            
            # Add final calculation explanation
            if len(risk_factors) > 0:
                risk_factors.append(
                    f"Final Score: {confidence_score:.1%} "
                    f"(Weighted average calculation)"
                )
            
            # Map decision to recommendation
            decision_map = {
                'BLOQUEAR': 'BLOCK - High fraud risk detected',
                'REVISAR': 'REVIEW - Manual review required', 
                'MONITOREAR': 'MONITOR - Monitor customer activity',
                'OK': 'APPROVE - Low fraud risk'
            }
            
            recommendation = decision_map.get(result['decision'], result['accion_recomendada'])
            
            return FraudAnalysisResponse(
                is_fraud=is_fraud,
                confidence_score=confidence_score,
                risk_factors=risk_factors,
                recommendation=recommendation,
                decision=result['decision']
            )
            
        except Exception as e:
            print(f"❌ Analysis error: {e}")
            print(f"🔍 Error type: {type(e).__name__}")
            import traceback
            print(f"📋 Stack trace:")
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

# Initialize the fraud system
print("🚀 Starting fraud_system_v2 module initialization...")
print(f"📊 Environment variables:")
print(f"   AWS_REGION: {os.getenv('AWS_REGION', 'not set')}")
print(f"   S3_BUCKET: {os.getenv('S3_BUCKET', 'not set')}")
print(f"   S3_FILE: {os.getenv('S3_FILE', 'not set')}")
print(f"   AWS_EXECUTION_ENV: {os.getenv('AWS_EXECUTION_ENV', 'not set')}")

fraud_system = FraudSystemV2()
print("✅ Module initialization completed")

@app.post("/analyze-fraud", response_model=FraudAnalysisResponse)
async def analyze_fraud(request: FraudAnalysisRequest):
    """Analyze fraud using multi-agent system"""
    return fraud_system.analyze_transaction(request)

@app.post("/decide", response_model=FraudAnalysisResponse)
async def make_fraud_decision(request: FraudAnalysisRequest):
    """Legacy endpoint compatibility"""
    return fraud_system.analyze_transaction(request)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    status = "healthy" if fraud_system.master_agent else "unhealthy"
    
    response = {
        "status": status,
        "service": "fraud-system-v2",
        "agents": "multi-agent" if fraud_system.master_agent else "unavailable",
        "initialization": "success" if fraud_system.master_agent else "failed"
    }
    
    if fraud_system.master_agent:
        try:
            response["s3_bucket"] = fraud_system.master_agent.bucket
            response["s3_file"] = fraud_system.master_agent.file_key
            response["data_records"] = len(fraud_system.master_agent.data)
            response["blacklist_count"] = len(fraud_system.master_agent.agente_blacklist.blacklist)
            response["fraud_average"] = fraud_system.master_agent.agente_fraude.promedio_fraude
        except Exception as e:
            response["agent_error"] = str(e)
    
    print(f"🏥 Health check: {response}")
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)