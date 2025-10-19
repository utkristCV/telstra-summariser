# Use an official Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy app files
COPY . .

# Expose port
EXPOSE 8000

# # Run the app
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"
ENV GUNICORN_CMD_ARGS="-k uvicorn.workers.UvicornWorker -w 2 -t 300 -b 0.0.0.0:8000"
CMD ["gunicorn", "main:app"]