import base64
from typing import Literal

from playwright.async_api import async_playwright

from pypaperflow.logger import setup_logger

logger = setup_logger(__name__)


async def create_pdf_from_html(
    content: str, type: Literal["html", "url"] = "html", output_path: str = None
) -> str:
    """Create an A4 PDF from an HTML string using Chromium via Playwright and returns it as a base64 encoded string.

    Args:
        html_content: The HTML content as a string.

    Returns:
        str: The PDF content as a base64 encoded string.

    """
    async with async_playwright() as p:
        # Launch Chromium browser. Headless=True runs it without a visible UI window.
        # Use channel="chrome" if you prefer to use an installed Google Chrome browser,
        # but using the bundled chromium is generally more reliable for automation.
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            # Set the HTML content for the page
            # Using page.set_content is good for self-contained HTML strings.
            if type == "html":
                await page.set_content(content, wait_until="networkidle")
            elif type == "url":
                await page.goto(content, wait_until="networkidle")

            logger.info("Generating PDF")

            # Generate the PDF as bytes
            pdf_bytes = await page.pdf(
                format="A4",  # Specify the page size
                print_background=True,  # Include background graphics and colors
                margin={  # Optional: Define margins (in pixels, mm, cm, or inches)
                    "top": "20mm",
                    "bottom": "20mm",
                    "left": "15mm",
                    "right": "15mm",
                },
                # Other useful options:
                # landscape=False,        # Set to True for landscape orientation
                # scale=1.0,              # Scale rendering (e.g., 0.8 for 80%)
                # header_template="<div></div>", # HTML template for header
                # footer_template="<div></div>", # HTML template for footer
                # display_header_footer=False # Set to True if using templates
            )

            if output_path:
                with open(output_path, "wb") as f:
                    f.write(pdf_bytes)
                return None

            # Convert bytes to base64 string
            base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
            return base64_pdf

        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise
        finally:
            # Ensure the browser is closed even if errors occur
            await browser.close()
