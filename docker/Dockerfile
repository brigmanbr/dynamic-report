# Base image for both production and testing
FROM python:3.9-slim AS base

# Set the working directory
WORKDIR /app

# Copy dependencies
COPY src/requirements.txt .
COPY src/requirements-test.txt .

# Install base dependencies
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app

# Install test dependencies in a separate stage for local testing
FROM base AS test
RUN pip install --no-cache-dir -r requirements-test.txt

# Copy the application code
COPY src/ .

# Command to run the application (default to production)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Add a testing entrypoint
FROM test AS dev
CMD ["pytest", "--maxfail=1", "--disable-warnings"]
