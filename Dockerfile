FROM python:3.11-slim

# Install git (needed for GitHub operations)
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy source code
COPY . /app/

# Install package and dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r pr_diff_bot/requirements.txt && \
    pip install -e .
COPY entrypoint.sh .

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

# Set Python path to include root directory
ENV PYTHONPATH=/app

# Run the script
ENTRYPOINT ["/app/entrypoint.sh"]
