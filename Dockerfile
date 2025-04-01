FROM python:3.9-slim

# Set Python to run in unbuffered mode
ENV PYTHONUNBUFFERED=1

# Create and set the working directory in the container
WORKDIR /app

# Copy requirements file into the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . /app/

# Ensure you're in the correct directory
WORKDIR /app

# Run tests (adjust this based on your directory structure)
RUN pytest --maxfail=1 --disable-warnings -q

# Expose port
EXPOSE 8080

# Run the application with gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
