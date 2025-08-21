from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import asyncio
from typing import Dict, Any
import os

app = FastAPI(title="Fraud Detection API Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FraudAnalysisRequest(BaseModel):
    customer_id: str
    transaction_id: str
    transaction_data: Dict[str, Any]

class FraudAnalysisResponse(BaseModel):
    is_fraud: bool
    confidence_score: float
    risk_factors: list
    recommendation: str

@app.post("/api/analyze-fraud", response_model=FraudAnalysisResponse)
async def analyze_fraud(request: FraudAnalysisRequest):
    """Main endpoint to analyze potential fraud"""
    try:
        # Orchestrate the fraud detection process
        async with httpx.AsyncClient() as client:
            # Step 1: Collect data from multiple sources
            data_response = await client.post(
                "http://data-collector:8001/collect",
                json={"customer_id": request.customer_id, "transaction_id": request.transaction_id}
            )
            
            # Step 2: Analyze patterns
            pattern_response = await client.post(
                "http://pattern-analyzer:8002/analyze",
                json={"transaction_data": request.transaction_data}
            )
            
            # Step 3: Make fraud decision
            fraud_response = await client.post(
                "http://fraud-agent:8003/decide",
                json={
                    "customer_data": data_response.json(),
                    "pattern_analysis": pattern_response.json(),
                    "transaction_data": request.transaction_data
                }
            )
            
            return fraud_response.json()
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "api-gateway"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)