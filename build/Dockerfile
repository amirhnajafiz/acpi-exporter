# Build stage
FROM python:3.11-slim AS build

# Set working directory
WORKDIR /build

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-compile --prefix=/install -r requirements.txt

# Final stage
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy installed dependencies from the build stage
COPY --from=build /install /usr/local

# Copy application source code
COPY src/ ./src

# Use a non-root user for better security
RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser

# Define entrypoint
ENTRYPOINT ["python", "src/main.py"]
