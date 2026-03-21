# Dockerfile for Parma - Python to SQF Transpiler
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy Python project files first for better caching
COPY pyproject.toml ./

# Install Python dependencies
RUN pip install --upgrade pip && pip install -e .

# Copy the rest of the application
COPY . .

# Create a directory for projects
RUN mkdir /workspace
WORKDIR /workspace

# Default command
CMD ["parma", "--help"]