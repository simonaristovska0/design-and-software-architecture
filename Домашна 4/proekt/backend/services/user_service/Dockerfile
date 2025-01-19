# Base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy only the necessary files
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose the port for the service
EXPOSE 8002

# Run the user service
CMD ["python", "manage.py", "runserver", "0.0.0.0:8002"]