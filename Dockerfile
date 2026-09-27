# Use official Python 3.11 image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install build dependencies (required for some Python packages like bcrypt)
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy only the requirements first to leverage Docker cache
# Wait, this project uses pyproject.toml / pip install -e .
# So we copy pyproject.toml first
COPY pyproject.toml ./

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Create a dummy src directory so `pip install -e .` doesn't fail before code is copied
RUN mkdir -p src/brandforge && touch src/brandforge/__init__.py

# Install project dependencies
# We also explicitly install the additional packages added during development
RUN pip install --no-cache-dir .
RUN pip install --no-cache-dir sqlmodel passlib[bcrypt] python-jose "pydantic[email]" python-multipart "bcrypt<4.0.0"

# Now copy the rest of the application code
COPY . .

# Ensure data directory exists for SQLite
RUN mkdir -p data

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "brandforge.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
