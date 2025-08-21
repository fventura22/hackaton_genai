from fastapi import FastAPI
from pydantic import BaseModel
import pika
import json
import asyncio
from typing import Dict, Any

app = FastAPI(title="Notification Service")

class NotificationRequest(BaseModel):
    recipient: str
    message: str
    priority: str = "normal"
    channel: str = "email"

class NotificationService:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.setup_rabbitmq()
    
    def setup_rabbitmq(self):
        try:
            self.connection = pika.BlockingConnection(
                pika.URLParameters("amqp://fraud_user:fraud_pass@rabbitmq:5672")
            )
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue='fraud_alerts', durable=True)
        except Exception as e:
            print(f"RabbitMQ connection failed: {e}")
    
    async def send_fraud_alert(self, alert_data: Dict[str, Any]):
        """Send fraud alert notification"""
        try:
            message = {
                "type": "fraud_alert",
                "customer_id": alert_data.get("customer_id"),
                "transaction_id": alert_data.get("transaction_id"),
                "risk_score": alert_data.get("risk_score"),
                "timestamp": alert_data.get("timestamp"),
                "recommendation": alert_data.get("recommendation")
            }
            
            if self.channel:
                self.channel.basic_publish(
                    exchange='',
                    routing_key='fraud_alerts',
                    body=json.dumps(message),
                    properties=pika.BasicProperties(delivery_mode=2)
                )
            
            # Simulate sending email/SMS
            await self.send_email_notification(message)
            await self.send_sms_notification(message)
            
            return {"status": "sent", "message": "Fraud alert sent successfully"}
        
        except Exception as e:
            return {"status": "error", "message": f"Failed to send alert: {str(e)}"}
    
    async def send_email_notification(self, message: Dict[str, Any]):
        """Simulate email notification"""
        await asyncio.sleep(0.1)
        print(f"EMAIL SENT: Fraud alert for transaction {message['transaction_id']}")
    
    async def send_sms_notification(self, message: Dict[str, Any]):
        """Simulate SMS notification"""
        await asyncio.sleep(0.1)
        print(f"SMS SENT: High risk transaction detected - {message['transaction_id']}")

notification_service = NotificationService()

@app.post("/send-alert")
async def send_fraud_alert(alert_data: Dict[str, Any]):
    """Send fraud alert notification"""
    return await notification_service.send_fraud_alert(alert_data)

@app.post("/send-notification")
async def send_notification(request: NotificationRequest):
    """Send general notification"""
    # Simulate notification sending
    await asyncio.sleep(0.1)
    return {
        "status": "sent",
        "recipient": request.recipient,
        "channel": request.channel,
        "message": "Notification sent successfully"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "notification-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)