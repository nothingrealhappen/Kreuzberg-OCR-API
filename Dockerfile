FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
	pandoc \
	tesseract-ocr \
	tesseract-ocr-eng \
	tesseract-ocr-deu \
	tesseract-ocr-fra \
	tesseract-ocr-spa \
	tesseract-ocr-chi-sim \
	tesseract-ocr-chi-tra \
	# Additional dependencies that might be needed
	build-essential \
	libpoppler-cpp-dev \
	pkg-config \
	python3-dev \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 