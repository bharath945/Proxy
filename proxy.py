from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os

app = FastAPI(
    title="Proxy API",
    description="Proxy service that forwards requests to the backend MCP API.",
    version="1.0.0"
)

# Allow CORS (you can restrict this in production if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to your frontend domain in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Backend API URL
BACKEND_URL = "https://dev-api-gateway.aesthatiq.com/mcp-service/ask"


@app.post("/mcp-service/ask")
async def proxy_ask(request: Request):
    """Proxy endpoint that forwards requests to the MCP backend."""
    body = await request.json()

    async with httpx.AsyncClient(verify=False) as client:
        response = await client.post(BACKEND_URL, json=body)

    return response.json()
