# Step 1: Start from an official, optimized lightweight Python base layer
FROM python:3.11-slim

# Step 2: Set the working directory inside the virtual filesystem of the container
WORKDIR /app

# Step 3: Copy our local app.py script into the container's working directory
COPY app.py .

# Step 4: Define the command that executes automatically when the container boots up
CMD ["python", "app.py"]