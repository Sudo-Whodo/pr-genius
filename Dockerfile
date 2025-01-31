FROM python:3.11-slim

# Install git (needed for gitpython)
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY pr-diff-bot/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the bot code
COPY pr-diff-bot/ .
COPY entrypoint.sh .

# Make entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]