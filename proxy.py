from fastapi import FastAPI, Request
import httpx
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Proxy API", description="SSL proxy for MCP service")

# Allow CORS (optional, but usually needed for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict to your frontend domain in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MCP API endpoint
MCP_URL = "https://dev-api-gateway.aesthatiq.com/mcp-service/ask"

@app.post("/ask")
async def proxy_ask(request: Request):
    """Proxy endpoint that forwards request to MCP API."""
    body = await request.json()

    async with httpx.AsyncClient(verify=False) as client:
        response = await client.post(MCP_URL, json=body)

    return response.json()
