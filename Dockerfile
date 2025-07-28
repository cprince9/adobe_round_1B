# Use an AMD64-compatible base image with Python
FROM --platform=linux/amd64 python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy rest of the source code
COPY . .

# Expose the port if needed (optional)
# EXPOSE 8080

# Set the entry point (update if needed)
CMD ["python", "main.py"]
