# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install the MariaDB C connector and other dependencies
RUN apt-get update && apt-get install -y \
    mariadb-client \
    libmariadb-dev \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install packaging faker
RUN pip install -r requirements.txt

# Copy the current directory contents into the container
COPY . .
# # RUN python /app/db/setup/test_connection.py
# RUN python /app/db/setup/create_db.py
# RUN python /app/db/setup/data_population.py

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=appserver.py

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"]
