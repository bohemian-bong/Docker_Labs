# Use an appropriate base image with Python installed
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the server files into the container
COPY app.py /app

# Install Flask
RUN pip install Flask

# Expose port 5000 for the Flask application
EXPOSE 5000

# Specify the command to run the server
CMD ["python", "app.py"]

