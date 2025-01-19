# Base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app/backend/services/data_service

# Copy only the necessary files
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Set the PYTHONPATH to include the project root
ENV PYTHONPATH="/app"

# Expose the port for the service
EXPOSE 8001

# Run the data service
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]