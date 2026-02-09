FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY scraper.py .
COPY validate_feed.py .

# Create volume mount point for feed.xml
VOLUME /app

# Set timezone
ENV TZ=UTC

# Run scraper
CMD ["python", "scraper.py"]
