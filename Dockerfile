# Use Python 3.9 slim as base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the service package
COPY service/ service/

# Create non-root user
RUN useradd -m -u 1000 theia
RUN chown -R theia:theia /app
USER theia

# Expose port
EXPOSE 8080

# Run gunicorn
CMD ["gunicorn", "--bind=0.0.0.0:8080", "--log-level=info", "service:app"]