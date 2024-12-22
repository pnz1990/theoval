# Builder stage to prepare the application
FROM python:3.8-slim as builder

# Set working directory
WORKDIR /build

# Install dos2unix for converting line endings
RUN apt-get update && \
    apt-get install -y dos2unix

# Copy all files to the builder
COPY . .

# Convert line endings and make scripts executable
RUN dos2unix entrypoint.sh healthcheck.sh && \
    chmod +x entrypoint.sh healthcheck.sh

# Final stage for the runtime environment
FROM python:3.8-slim

# Install necessary packages and upgrade pip
RUN apt-get update && \
    apt-get install -y postgresql-client curl && \
    pip install --upgrade pip

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy built files from the builder stage
COPY --from=builder /build .

# Expose the application port
EXPOSE 5000

# Define entrypoint and default command
ENTRYPOINT ["/bin/sh"]
CMD ["/app/entrypoint.sh"]