# Use official Python 3.11 image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install build dependencies (required for some Python packages like bcrypt)
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy the entire project code first
COPY . .

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Install the project and all its dependencies correctly
RUN pip install --no-cache-dir .
RUN pip install --no-cache-dir sqlmodel passlib[bcrypt] python-jose "pydantic[email]" python-multipart "bcrypt<4.0.0"

# Ensure data directory exists for SQLite
RUN mkdir -p data

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "brandforge.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
