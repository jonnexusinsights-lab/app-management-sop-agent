import typer
import uvicorn
from src.ingestion.pipeline import ingestion_pipeline
from src.agent.core import sop_agent

app = typer.Typer()

@app.command()
def start():
    """
    Starts the API server.
    """
    print("Starting SOP Agent API Server...")
    uvicorn.run("src.api.server:app", host="0.0.0.0", port=8000, reload=True)

@app.command()
def ingest(file_path: str = typer.Option(None, help="Path to a file to ingest (optional)"),
           text: str = typer.Option(None, help="Raw text to ingest (optional)")):
    """
    Ingests a document into the Knowledge Base.
    """
    if file_path:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        ingestion_pipeline.ingest_from_text(content, source=file_path)
        print(f"Successfully ingested file: {file_path}")
    elif text:
        ingestion_pipeline.ingest_from_text(text, source="cli_input")
        print("Successfully ingested text.")
    else:
        print("Please provide either --file-path or --text.")

@app.command()
def query(question: str):
    """
    Asks a question to the SOP Agent directly.
    """
    response = sop_agent.process_request(question)
    print(f"\nAnswer:\n{response}\n")

if __name__ == "__main__":
    app()
