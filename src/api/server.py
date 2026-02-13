from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.agent.core import sop_agent
from src.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API for the Managerial SOP Assistant"
)

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: str

@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy"}

@app.post("/chat", response_model=QueryResponse)
async def chat(request: QueryRequest):
    """
    Chat endpoint for managers.
    """
    try:
        # Process the query through the agent
        response = sop_agent.process_request(request.query)
        return QueryResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
