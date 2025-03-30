from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .html2pdf import create_pdf_from_html
from .word2html import convert_word_to_pdf

app = FastAPI()


class PDFRequest(BaseModel):
    """Request body for the HTML to PDF conversion service."""

    content: str
    type: Literal["html", "url"] = "html"


class WordRequest(BaseModel):
    """Request body for the Word to PDF conversion service."""

    content: str  # base64 encoded Word document


@app.get("/")
async def root():
    """Root endpoint for the HTML to PDF conversion service."""
    return {"message": "HTML to PDF conversion service"}


@app.post("/convert-html")
async def generate_pdf(request: PDFRequest):
    """Generate a PDF from an HTML string or URL.

    Args:
        request: PDFRequest containing content and type

    Returns:
        pdf: str
        message: str

    """
    try:
        base64_pdf = await create_pdf_from_html(request.content, request.type)
        return {"pdf": base64_pdf, "message": "PDF generated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/convert-word")
async def convert_word(request: WordRequest):
    """Convert a base64 encoded Word document to PDF.

    Args:
        request: WordRequest containing base64 encoded Word document

    Returns:
        pdf: str
        message: str

    """
    try:
        # Convert base64 Word to PDF
        base64_pdf = await convert_word_to_pdf(request.content)

        return {
            "pdf": base64_pdf,
            "message": "Word document converted to PDF successfully",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
