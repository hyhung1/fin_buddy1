import asyncio
import logging
import sys
import glob
import os
from pathlib import Path
from typing import Dict, List, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn

from financial_data_analysis_app import FinancialDataAnalysisApp
from services.excel_header_detection import process_uploaded_file

# -----------------------------------------------------------------------------
# Environment & logging
# -----------------------------------------------------------------------------
load_dotenv()

# Custom filter to exclude LLM request logs
class LLMRequestFilter(logging.Filter):
    def filter(self, record):
        msg = record.getMessage()
        return not (
            "LLM Request:" in msg or 
            "System Instruction:" in msg or
            "FINANCIAL-PANDAS-EXPERT" in msg or
            "Guidelines:" in msg
        )

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else sys.stdout)],
)
logger = logging.getLogger("fin_buddy_backend")
logger.addFilter(LLMRequestFilter())

# -----------------------------------------------------------------------------
# FastAPI app
# -----------------------------------------------------------------------------
app = FastAPI(title="Financial CSV Buddy API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: lock down in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Folder to keep user uploads
UPLOADS_DIR = Path(__file__).parent / "uploads"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

# Create the generated scripts directory if it doesn't exist
GENERATED_SCRIPTS_DIR = Path("gen_scripts_csv_arti_v2_4").resolve()
GENERATED_SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)

# Mount the scripts directory to serve static files
app.mount("/static", StaticFiles(directory=str(GENERATED_SCRIPTS_DIR)), name="static")

# -----------------------------------------------------------------------------
# In-memory session store  (session_id → FinancialDataAnalysisApp)
# -----------------------------------------------------------------------------
session_apps: Dict[str, FinancialDataAnalysisApp] = {}

# -----------------------------------------------------------------------------
# Pydantic models (kept close to the ones used in the client)
# -----------------------------------------------------------------------------
class UploadResponse(BaseModel):
    session_id: str
    file_name: str
    message: str
    # legacy / optional fields kept for client compatibility
    file_id: Optional[str] = None
    headers: Optional[List[str]] = None
    analysis: Optional[dict] = None


class MessageV1(BaseModel):
    content: str
    is_link: bool = False
    link: Optional[str] = None
    images: List[str] = []  # New field to store image paths


class ChatRequestV1(BaseModel):
    session_id: str
    message: str


class ChatResponseV1(BaseModel):
    session_id: str
    response: MessageV1
    events: List[dict] = []
    analysis: Optional[dict] = None
    images: List[str] = []  # Add this field to the response

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
async def _persist_to_csv(upload: UploadFile) -> Path:
    """Detect the correct header row, persist as CSV, and return absolute Path."""

    try:
        _, header_row, output_path = await process_uploaded_file(upload, UPLOADS_DIR)
        logger.info(
            f"Processed upload '{upload.filename}' (header row #{header_row}) → "
            f"{output_path.relative_to(UPLOADS_DIR.parent)}"
        )
        return output_path
    finally:
        # Ensure file stream is closed regardless of outcome
        await upload.close()

# -----------------------------------------------------------------------------
# Routes
# -----------------------------------------------------------------------------
@app.post("/api/upload_v1", response_model=UploadResponse)
async def upload_v1(file: UploadFile = File(...)):
    csv_path = await _persist_to_csv(file)

    # Create new ADK analysis session
    analysis_app = FinancialDataAnalysisApp(csv_file=str(csv_path))
    session_apps[analysis_app.session_id] = analysis_app

    # Kick off the artefact upload + LLM priming step in the background so the
    # dataset is ready by the time the user submits their first question.  We
    # use *run_in_executor* to avoid blocking the request-response cycle.
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, analysis_app.ensure_artifact_uploaded)

    return UploadResponse(
        session_id=analysis_app.session_id,
        file_name=file.filename,
        message="File processed successfully. Ask your questions!",
    )


@app.get("/images/{folder}/{subfolder}/{filename}")
async def get_image(folder: str, subfolder: str, filename: str):
    image_path = GENERATED_SCRIPTS_DIR / folder / subfolder / filename
    if not image_path.exists() or not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(str(image_path), media_type="image/png")


@app.post("/api/chat_v1", response_model=ChatResponseV1)
async def chat_v1(req: ChatRequestV1):
    app_instance = session_apps.get(req.session_id)
    if app_instance is None:
        raise HTTPException(status_code=404, detail="Session not found. Please upload a file first.")

    # The heavy lifting (LLM calls, pandas execution) is blocking – run it in a thread
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, app_instance.run_flow, [req.message])

    outputs = result.get("analysis_outputs", [])
    answer_text = outputs[0] if outputs else "No answer could be generated."
    
    # Find any generated PNG images
    images = []
    output_folder = result.get("output_folder_name")
    if output_folder:
        output_path = Path(output_folder)
        # Search for PNG files in phase_2 folders
        for phase2_dir in output_path.glob("*_phase_2"):
            for png_file in phase2_dir.glob("*.png"):
                # Create both paths - one for the Express static server and one for our direct endpoint
                folder_name = output_path.name
                subfolder_name = phase2_dir.name
                file_name = png_file.name
                
                # Primary path using Express static file server
                image_url = f"/generated-files/{folder_name}/{subfolder_name}/{file_name}"
                
                # Fallback path using our direct endpoint
                fallback_url = f"/images/{folder_name}/{subfolder_name}/{file_name}"
                
                images.append(image_url)

    return ChatResponseV1(
        session_id=req.session_id,
        response=MessageV1(
            content=answer_text,
            images=images
        ),
        events=[],
        analysis=result,
        images=images
    )


# -----------------------------------------------------------------------------
# Entrypoint (only used when run directly – the Node proxy spawns this script)
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info") 