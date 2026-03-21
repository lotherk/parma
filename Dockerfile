# Dockerfile for Rarma - Ruby ArmA Transpiler
FROM ruby:2.7-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy gem files first for better caching
COPY rarma.gemspec Gemfile* ./

# Install bundler and dependencies
RUN gem install bundler && bundle install

# Copy the rest of the application
COPY . .

# Build and install the rarma gem
RUN gem build rarma.gemspec && gem install rarma-*.gem

# Create a directory for projects
RUN mkdir /workspace
WORKDIR /workspace

# Default command
CMD ["rarma", "--help"]