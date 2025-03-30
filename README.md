# PyPaperFlow Service

A FastAPI-based service that converts URLs, HTML and Word content to PDF documents.

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
![GitHub License](https://img.shields.io/github/license/bselleslagh/PyPaperFlow)
![GitHub Release](https://img.shields.io/github/v/release/bselleslagh/PyPaperFlow)
![X (formerly Twitter) Follow](https://img.shields.io/twitter/follow/BenSelleslagh)

## Features

- Convert HTML content to PDF
- Convert URLs to PDF
- Convert Word documents to PDF
- A4 format with customizable margins
- Background graphics and colors support
- Asynchronous processing
- Base64 encoded output

## Installation

1. Clone the repository:
```bash
git clone https://github.com/bselleslagh/PyPaperFlow.git
cd PyPaperFlow
```

2. Install dependencies using UV:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

3. Install Playwright browsers:
```bash
playwright install
```

4. Set up pre-commit hooks:
```bash
# Install the pre-commit hooks
uv run pre-commit install

# Run pre-commit on all files (optional)
uv run pre-commit run --all-files
```

## Docker Installation

```bash
docker build -t pypaperflow .
docker run -p 8000:8000 pypaperflow
```

## Usage

The service exposes three endpoints:

### Root Endpoint

```http
GET /
```

Returns a welcome message confirming the service is running.

### Convert HTML/URL to PDF Endpoint

```http
POST /convert-html
```

Request body:
```json
{
    "content": "string",
    "type": "html" | "url"
}
```

- `content`: HTML string or URL to convert
- `type`: Either "html" for HTML content or "url" for web pages (default: "html")

Response:
```json
{
    "pdf": "base64_encoded_string",
    "message": "PDF generated successfully"
}
```

### Convert Word to PDF Endpoint

```http
POST /convert-word
```

Request body:
```json
{
    "content": "string"  // base64 encoded Word document
}
```

Response:
```json
{
    "pdf": "base64_encoded_string",
    "message": "Word document converted to PDF successfully"
}
```

## Example

```python
import requests
import base64

# Convert HTML to PDF
url = "http://localhost:8000/convert-html"
payload = {
    "content": "<h1>Hello World</h1>",
    "type": "html"
}
response = requests.post(url, json=payload)
pdf_data = response.json()["pdf"]

# Convert Word to PDF
with open("document.docx", "rb") as word_file:
    word_base64 = base64.b64encode(word_file.read()).decode("utf-8")

payload = {
    "content": word_base64
}
response = requests.post("http://localhost:8000/convert-word", json=payload)
pdf_data = response.json()["pdf"]
```

## Requirements

- Python ≥ 3.13
- FastAPI
- Playwright
- See `pyproject.toml` for full dependencies

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Ben Selleslagh ([@BenSelleslagh](https://twitter.com/BenSelleslagh))

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.