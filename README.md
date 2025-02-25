# Kreuzberg OCR API

A Docker-based API server for OCR (Optical Character Recognition) from PDF and image files using the Kreuzberg library.

## Features

- Extract text from PDF documents and images (PNG, JPG, TIFF)
- RESTful API with FastAPI
- Multilingual support (English, German, French, Spanish)
- Dockerized for easy deployment
- Asynchronous processing

## Requirements

- Docker
- Docker Compose (optional, for easier management)

## Quick Start

### Using Docker

1. Build the Docker image:

```bash
docker build -t kreuzberg-ocr-api .
```

2. Run the container:

```bash
docker run -p 8000:8000 kreuzberg-ocr-api
```

3. The API will be available at http://localhost:8000

### Using Docker Compose

1. Use the provided `docker-compose.yml` file:

```yaml
version: "3"

services:
  ocr-api:
    build: .
    ports:
      - "8000:8000"
    restart: unless-stopped
    volumes:
      - ./logs:/app/logs
    environment:
      - LOG_LEVEL=INFO
```

2. Start the service:

```bash
docker-compose up -d
```

## API Usage

### API Documentation

Once the server is running, you can access the interactive API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Extract Text from a PDF or Image

```bash
curl -X POST "http://localhost:8000/extract_text" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_document.pdf" \
  -F "language=eng"
```

#### Parameters:

- `file`: The PDF or image file to process (required)
  - Supported formats: PDF, PNG, JPG/JPEG, TIFF/TIF
- `language`: Language code for OCR (optional, defaults to English)
  - Available languages: `eng` (English), `deu` (German), `fra` (French), `spa` (Spanish)

#### Response:

```json
{
  "filename": "your_document.pdf",
  "text": "Extracted text content from the document..."
}
```

### Using the Test Script

The repository includes a test script (`test_api.py`) that demonstrates how to use the API programmatically:

```bash
python test_api.py path/to/your/document.pdf --language eng
```

Optional parameters:

- `--url`: Custom API endpoint URL (default: http://localhost:8000/extract_text)
- `--output`: Path to save the extracted text (optional)

## Technical Details

### How It Works

1. The API receives a PDF or image file through the `/extract_text` endpoint
2. It determines the MIME type of the file based on its extension
3. The file content is passed to Kreuzberg's `extract_bytes` function along with the MIME type
4. Kreuzberg processes the file using Tesseract OCR and returns the extracted text
5. The API returns the text in a JSON response

### Dependencies

- **System Dependencies**:

  - Pandoc (minimum version 2)
  - Tesseract OCR (minimum version 5)
  - Language packs for Tesseract

- **Python Dependencies**:
  - FastAPI: Web framework
  - Uvicorn: ASGI server
  - Kreuzberg: OCR library
  - Python-multipart: For handling file uploads
  - Pydantic: For data validation

## Adding More Languages

To add support for additional languages, modify the Dockerfile to install more Tesseract language packs:

```dockerfile
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-deu \
    tesseract-ocr-fra \
    tesseract-ocr-spa \
    tesseract-ocr-ita \  # Add Italian
    tesseract-ocr-por \  # Add Portuguese
    # Add more languages as needed
```

## Development

### Local Setup

1. Clone the repository
2. Install the required system dependencies:

   - Pandoc (minimum version 2)
   - Tesseract OCR (minimum version 5)
   - Required development libraries

3. Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

4. Run the application:

```bash
uvicorn main:app --reload
```

## Troubleshooting

### Common Issues

1. **Error: "extract_bytes() missing 1 required positional argument: 'mime_type'"**

   - This error occurs if the API cannot determine the MIME type of the uploaded file.
   - Make sure the file has a proper extension (.pdf, .png, .jpg, .tiff).

2. **OCR quality issues**

   - Try specifying the correct language parameter for your document.
   - Ensure the document is of good quality and properly scanned.

3. **Docker build fails**
   - Make sure you have sufficient disk space and memory.
   - Check if all required system dependencies are available.

## License

MIT

## Acknowledgements

This project uses the [Kreuzberg](https://github.com/goldziher/kreuzberg) library for OCR processing.
