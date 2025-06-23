FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js (required for Claude Code)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# Install Claude Code CLI
RUN npm install -g @anthropic-ai/claude-code

# Install uv package manager
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:$PATH"

# Create workspace directory
WORKDIR /workspace

# Copy project files
COPY pyproject.toml .

# Install Python dependencies with uv
RUN uv sync

# Set up git configuration for the container
RUN git config --global --add safe.directory /workspace

# Expose common development ports
EXPOSE 8000 8080 3000

# Set the default shell
SHELL ["/bin/bash", "-c"]