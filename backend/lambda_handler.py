"""AWS Lambda handler for FastAPI application."""

from mangum import Mangum
from app.app import app

# Create the Mangum handler that wraps the FastAPI app
# This makes FastAPI compatible with AWS Lambda and API Gateway
handler = Mangum(app, lifespan="off")

# For local testing
if __name__ == "__main__":
    import uvicorn

    # Run locally with: python lambda_handler.py
    uvicorn.run(app, host="0.0.0.0", port=8000)
