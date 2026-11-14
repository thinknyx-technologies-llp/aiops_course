from fastapi import FastAPI, HTTPException
import logging
import time

app = FastAPI(title="Payment Service")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("payment-service")


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/charge")
def process_payment(mode: str = "normal"):

    logger.info("Processing payment. Mode: %s", mode)

    if mode == "slow":
        time.sleep(5)
        logger.warning("Payment processing was slow")

    if mode == "fail":
        logger.error("Payment transaction failed")
        raise HTTPException(
            status_code=500,
            detail="Simulated payment failure"
        )

    return {
        "payment_status": "completed",
        "mode": mode
    }
