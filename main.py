from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from kreuzberg import extract_bytes
import logging
from typing import Optional
import io
import mimetypes

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Kreuzberg OCR API",
    description="API for OCR from PDF images using Kreuzberg",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "message": "Kreuzberg OCR API is running"}

async def extract_text_from_bytes(content: bytes, mime_type: str, language: Optional[str] = None):
    """Extract text from bytes using Kreuzberg."""
    try:
        # Pass language parameter if provided
        kwargs = {}
        if language:
            kwargs["language"] = language
            
        result = await extract_bytes(content, mime_type, **kwargs)
        return result.content
    except Exception as e:
        logger.error(f"Error extracting text: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error extracting text: {str(e)}")

@app.post("/extract_text")
async def extract_text(
    file: UploadFile = File(...),
    language: Optional[str] = None
):
    """
    Extract text from a PDF file using OCR.
    
    - **file**: PDF file to process
    - **language**: Optional language code for OCR (e.g., 'eng', 'deu', 'fra', 'spa')
    """
    # Validate file type
    if not file.filename.lower().endswith((".pdf", ".png", ".jpg", ".jpeg", ".tiff", ".tif")):
        raise HTTPException(
            status_code=400, 
            detail="Only PDF and image files (PNG, JPG, TIFF) are accepted"
        )
    
    try:
        # Read file content
        content = await file.read()
        
        # Determine MIME type based on file extension
        mime_type = None
        if file.filename.lower().endswith(".pdf"):
            mime_type = "application/pdf"
        elif file.filename.lower().endswith((".png")):
            mime_type = "image/png"
        elif file.filename.lower().endswith((".jpg", ".jpeg")):
            mime_type = "image/jpeg"
        elif file.filename.lower().endswith((".tiff", ".tif")):
            mime_type = "image/tiff"
        else:
            # Use Python's mimetypes as fallback
            mime_type = mimetypes.guess_type(file.filename)[0]
            
        if not mime_type:
            raise HTTPException(status_code=400, detail="Could not determine file MIME type")
        
        # Process with Kreuzberg
        text = await extract_text_from_bytes(content, mime_type, language)
        
        return {"filename": file.filename, "text": text}
    except Exception as e:
        logger.error(f"Error processing file {file.filename}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False) 