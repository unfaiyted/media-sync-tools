# Use a base image with Python and Uvicorn pre-installed
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application directory to the container
COPY . .

# Expose the port that the application will run on
EXPOSE 8000

# Set the entrypoint command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
