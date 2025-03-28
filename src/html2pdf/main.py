from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .html2pdf import create_pdf_from_html

app = FastAPI()


class PDFRequest(BaseModel):
    """Request body for the HTML to PDF conversion service."""

    content: str
    type: Literal["html", "url"] = "html"


@app.get("/")
async def root():
    """Root endpoint for the HTML to PDF conversion service."""
    return {"message": "HTML to PDF conversion service"}


@app.post("/generate-pdf")
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
