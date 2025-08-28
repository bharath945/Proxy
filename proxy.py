from fastapi import FastAPI, Request
import httpx
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Secure Proxy", description="HTTPS proxy for MCP service")

# Allow CORS so Flutter can call it
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in prod, restrict to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Your backend (NO SSL)
MCP_URL = "http://dev-api-gateway.aesthatiq.com/mcp-service/ask"

@app.post("/ask")
async def proxy_ask(request: Request):
    body = await request.json()

    # Forward to non-SSL backend
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(MCP_URL, json=body)

    return response.json()
