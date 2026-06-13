# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies for Playwright and building FAISS
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright Chromium (without system deps since we use slim which might need some tweaks, 
# but for HF spaces/Render it's often sufficient or we can use the official Playwright image)
# Actually, the official Playwright python image is better to avoid missing shared libraries.
# Let's switch base image in the next iteration if needed, but for now we'll just run install.
RUN playwright install chromium

# Copy the project files
COPY . .

# Pre-cache the Hugging Face model to avoid startup delays
# Requires --build-arg HF_TOKEN=<your_token> during build
ARG HF_TOKEN
ENV HF_TOKEN=$HF_TOKEN
RUN python -c "import os; from transformers import AutoModel, AutoTokenizer; t = os.environ.get('HF_TOKEN'); AutoTokenizer.from_pretrained('ai4bharat/indic-bert', token=t); AutoModel.from_pretrained('ai4bharat/indic-bert', token=t)"


# Ensure data directory exists
RUN mkdir -p data

# Expose port
EXPOSE 8000

# Run the FastAPI application using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
