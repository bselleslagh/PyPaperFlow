import base64
from io import BytesIO
from typing import Union

import mammoth

from .html2pdf import create_pdf_from_html
from .logger import setup_logger

logger = setup_logger(__name__)


async def convert_word_to_pdf(
    word_file: Union[str, bytes],
    output_path: Union[str, None] = None,
) -> Union[str, None]:
    """Convert a Word document to PDF using mammoth for HTML conversion and Playwright for PDF generation.

    Args:
        word_file: Base64 encoded string of the Word document or bytes of the Word document
        output_path: Optional path to save the PDF file. If not provided, returns base64 encoded PDF

    Returns:
        If output_path is provided, returns None. Otherwise returns the PDF as a base64 encoded string.

    """
    try:
        # Handle base64 encoded input
        if isinstance(word_file, str):
            try:
                word_file = base64.b64decode(word_file)
            except Exception as e:
                raise ValueError("Invalid base64 encoded string") from e

        # Convert Word to HTML using mammoth
        with BytesIO(word_file) as docx_file:
            result = mammoth.convert_to_html(docx_file)
        html_content = result.value

        # Convert HTML to PDF using the existing functionality
        base64_pdf = await create_pdf_from_html(html_content)

        # If output path is provided, save the PDF
        if output_path:
            pdf_bytes = base64.b64decode(base64_pdf)
            with open(output_path, "wb") as f:
                f.write(pdf_bytes)
            logger.info(f"PDF saved to {output_path}")
            return None

        return base64_pdf

    except Exception as e:
        logger.error(f"Error converting Word to PDF: {e}")
        raise
