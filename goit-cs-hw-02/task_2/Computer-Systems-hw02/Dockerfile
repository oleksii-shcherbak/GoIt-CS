# Use the official lightweight Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Install system-level dependencies required to build psycopg2 from source
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    python3-dev \
 && apt-get clean

# Copy Python dependencies file
COPY requirements.txt .

# Install Python dependencies from the file
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose the port on which Uvicorn will run
EXPOSE 8000

# Set the default command to run the FastAPI app with Uvicorn
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
