# Use the official Python image from DockerHub
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Set environment variable for API Key
ENV GEMINI_API_KEY=$GEMINI_API_KEY

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Expose the port the app will run on (adjust if needed)
EXPOSE 8080



# Run the Python application (adjust the entry point if needed)
CMD ["python", "main.py"]