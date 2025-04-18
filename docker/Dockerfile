# Use official slim Python image for smaller footprint
FROM python:3.10-slim

# Set environment variable BEFORE using it
ENV PYTHONPATH=/app/src:$PYTHONPATH

# Set working directory inside the container
WORKDIR /app

# Copy all project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

CMD ["bash"]
