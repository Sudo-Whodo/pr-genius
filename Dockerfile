FROM python:3.11-slim

# Install git (needed for GitHub operations)
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY pr_diff_bot/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Create directories
RUN mkdir -p /app/examples

# Copy application code
COPY pr_diff_bot/ .
COPY entrypoint.sh .

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

# Set Python path to include root directory
ENV PYTHONPATH=/app

# Run the script
ENTRYPOINT ["/app/entrypoint.sh"]
