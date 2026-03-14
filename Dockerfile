FROM python:3.11-slim

WORKDIR /app

# Copy requirements first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY prompt_router.py .
COPY .env.example .env

# Create a non-root user for security
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Set environment variable
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "prompt_router.py"]
