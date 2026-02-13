import os
import sys
from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn
from pathlib import Path

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.agent.core import sop_agent
from src.ingestion.pipeline import ingestion_pipeline
from src.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

# Setup templates and static files
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

class ChatRequest(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "project_name": settings.PROJECT_NAME})

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    from src.observability.logger import logger
    try:
        logger.info(f"API Request: POST /api/chat - Message length: {len(request.message)}")
        response = sop_agent.process_request(request.message)
        logger.info("API Response: Success")
        return {"response": response}
    except Exception as e:
        logger.error(f"API Error: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/api/ingest")
async def ingest_endpoint(
    text: str = Form(None),
    source_name: str = Form(...),
    file: UploadFile = File(None)
):
    from src.observability.logger import logger
    try:
        logger.info(f"API Request: POST /api/ingest - Source: {source_name}")

        if text:
            logger.info("Ingesting raw text...")
            ingestion_pipeline.ingest_from_text(text, source=source_name)
        elif file:
             logger.info(f"Ingesting file: {file.filename}")
             # Placeholder for file ingestion logic
             content = await file.read()
             text_content = content.decode("utf-8") # Simple decoding for text files
             ingestion_pipeline.ingest_from_text(text_content, source=source_name)
        else:
             logger.warning("No content provided for ingestion")
             return JSONResponse(status_code=400, content={"error": "No content provided"})

        # Reload RAGEngine
        from src.rag.engine import rag_engine
        if hasattr(rag_engine, 'reload'):
            logger.info("Reloading RAG Engine...")
            rag_engine.reload()

        logger.info(f"Successfully ingested '{source_name}'")
        return {"message": f"Successfully ingested '{source_name}'!"}

    except Exception as e:
        logger.error(f"Ingestion API Error: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

if __name__ == "__main__":
    # Ensure logs show up in console when running directly
    import logging
    logging.basicConfig(level=logging.INFO)
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True)
