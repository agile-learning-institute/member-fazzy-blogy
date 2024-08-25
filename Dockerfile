# Stage 1: Build backend
FROM python:3.12-slim as backend

# Install system dependencies
RUN apt-get update && apt-get install -y git

# Set the working directory in the container
WORKDIR /blogy

# Copy only the necessary files to the container
COPY requirements.txt .
COPY alembic.ini .
COPY api/ /blogy/api
COPY alembic/ /blogy/alembic

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run Alembic migrations
RUN alembic upgrade head

# Stage 2: Build frontend
FROM node:20-alpine as frontend

# Set the working directory in the container
WORKDIR /blogy/frontend

# Copy the frontend files to the container
COPY frontend/package.json frontend/package-lock.json ./
COPY frontend/ ./

# Install frontend dependencies and build the frontend
RUN npm install && npm run build

# Stage 3: Final stage
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /opt/blogy

# Copy the backend from the backend stage
COPY --from=backend /app /opt/blogy

# Copy the frontend build to the backend's static files directory
COPY --from=frontend /app/frontend/dist /opt/blogy/api/static

# Install Gunicorn and other necessary packages
RUN pip install gunicorn gevent

# Expose the port that Gunicorn will run on
EXPOSE 8080

# Set environment variables
ENV PYTHONPATH=/opt/blogy

# Command to run the backend using Gunicorn
CMD ["gunicorn", "--worker-class", "gevent", "--workers", "3", "--bind", "0.0.0.0:8080", "api.app:app"]
