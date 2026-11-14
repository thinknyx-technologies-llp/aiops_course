from fastapi import FastAPI, HTTPException
import requests
import logging
import time

app = FastAPI(title="Order Service")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("order-service")

PAYMENT_URL = "http://payment:8001/charge"


@app.get("/")
def home():
    return {"message": "Order service is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/order")
def create_order(mode: str = "normal"):
    logger.info("Received order request. Payment mode: %s", mode)

    try:
        response = requests.post(
            PAYMENT_URL,
            params={"mode": mode},
            timeout=15
        )

        response.raise_for_status()

        logger.info("Order processed successfully")

        return {
            "order_status": "success",
            "payment_response": response.json()
        }

    except requests.RequestException as error:
        logger.error("Payment processing failed: %s", error)

        raise HTTPException(
            status_code=502,
            detail="Payment service failed"
        )

@app.get("/cpu")
def cpu_load(seconds: int = 15):
    seconds = max(1, min(seconds, 30))

    end_time = time.time() + seconds
    value = 0

    while time.time() < end_time:
        value = (value * 13 + 7) % 1000003

    logger.warning("CPU load simulation completed")

    return {
        "status": "completed",
        "duration_seconds": seconds
    }