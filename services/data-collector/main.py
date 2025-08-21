from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
import httpx
from typing import Dict, Any
import random

app = FastAPI(title="Data Collection Service")

class DataCollectionRequest(BaseModel):
    customer_id: str
    transaction_id: str

class DataCollectionResponse(BaseModel):
    customer_profile: Dict[str, Any]
    transaction_history: list
    device_info: Dict[str, Any]
    external_data: Dict[str, Any]

class DataCollector:
    def __init__(self):
        self.external_apis = {
            "credit_bureau": "https://api.creditbureau.com",
            "device_fingerprint": "https://api.devicefingerprint.com",
            "geolocation": "https://api.geolocation.com"
        }
    
    async def get_customer_profile(self, customer_id: str) -> Dict[str, Any]:
        """Retrieve customer profile from internal database"""
        # Simulate database query
        await asyncio.sleep(0.1)
        
        # Mock customer data
        profiles = {
            "CUST001": {
                "customer_id": "CUST001",
                "account_age_days": 365,
                "avg_transaction_amount": 150.0,
                "frequent_locations": ["New York", "Boston"],
                "risk_score": 0.2,
                "account_status": "active"
            },
            "CUST002": {
                "customer_id": "CUST002",
                "account_age_days": 30,
                "avg_transaction_amount": 50.0,
                "frequent_locations": ["Miami"],
                "risk_score": 0.6,
                "account_status": "new"
            }
        }
        
        return profiles.get(customer_id, {
            "customer_id": customer_id,
            "account_age_days": random.randint(1, 1000),
            "avg_transaction_amount": random.uniform(50, 500),
            "frequent_locations": ["Unknown"],
            "risk_score": random.uniform(0, 1),
            "account_status": "active"
        })
    
    async def get_transaction_history(self, customer_id: str) -> list:
        """Retrieve recent transaction history"""
        await asyncio.sleep(0.1)
        
        # Mock transaction history
        return [
            {
                "transaction_id": f"TXN{i}",
                "amount": random.uniform(10, 1000),
                "timestamp": f"2024-01-{random.randint(1, 30)}T{random.randint(0, 23)}:00:00Z",
                "location": random.choice(["New York", "Boston", "Miami", "Unknown"]),
                "status": "completed"
            }
            for i in range(random.randint(5, 20))
        ]
    
    async def get_device_info(self, customer_id: str) -> Dict[str, Any]:
        """Retrieve device fingerprint information"""
        await asyncio.sleep(0.1)
        
        return {
            "device_id": f"DEV_{customer_id}",
            "device_type": random.choice(["mobile", "desktop", "tablet"]),
            "os": random.choice(["iOS", "Android", "Windows", "macOS"]),
            "browser": random.choice(["Chrome", "Safari", "Firefox", "Edge"]),
            "is_known_device": random.choice([True, False]),
            "risk_score": random.uniform(0, 1)
        }
    
    async def get_external_data(self, customer_id: str) -> Dict[str, Any]:
        """Collect data from external sources"""
        await asyncio.sleep(0.2)
        
        # Simulate external API calls
        return {
            "credit_score": random.randint(300, 850),
            "identity_verified": random.choice([True, False]),
            "watchlist_match": random.choice([True, False]),
            "geolocation_risk": random.uniform(0, 1)
        }
    
    async def collect_all_data(self, customer_id: str, transaction_id: str) -> DataCollectionResponse:
        """Collect data from all sources concurrently"""
        tasks = [
            self.get_customer_profile(customer_id),
            self.get_transaction_history(customer_id),
            self.get_device_info(customer_id),
            self.get_external_data(customer_id)
        ]
        
        results = await asyncio.gather(*tasks)
        
        return DataCollectionResponse(
            customer_profile=results[0],
            transaction_history=results[1],
            device_info=results[2],
            external_data=results[3]
        )

collector = DataCollector()

@app.post("/collect", response_model=DataCollectionResponse)
async def collect_data(request: DataCollectionRequest):
    """Collect data from multiple sources for fraud analysis"""
    return await collector.collect_all_data(request.customer_id, request.transaction_id)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "data-collector"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)