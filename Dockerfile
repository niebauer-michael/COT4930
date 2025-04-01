# Step 1: Use the official Python base image
FROM python:3.9-slim

# Step 2: Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Step 3: Create and set the working directory in the container
WORKDIR /app

# Step 4: Copy requirements file into the container
COPY requirements.txt /app/

# Step 5: Install dependencies including testing dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 6: Install testing dependencies (if not in requirements.txt)
# If you have a testing section in requirements.txt, you don't need this line
# RUN pip install pytest

# Step 7: Copy the rest of the application code into the container
COPY . /app/

# Step 8: Run tests (optional, if you want to run tests during build)
# This will run pytest and stop the build if tests fail
RUN pytest --maxfail=1 --disable-warnings -q

# Step 9: Expose the port your app will listen on
EXPOSE 8080

# Step 10: Run the application
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
