# Use Python 3.12-slim and strip unecessary OS packages - keeps the image small.
FROM python:3.12-slim

# Working directory inside the container. All subsequent commands operate relative to this path.
WORKDIR /app

# Copy only the requirements file first.
COPY requirements.txt .

# Install Python dependencies specified inside requirements.txt. --no-cahce-dir prevents pip from storing download cache.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of service's files into the container.
COPY . .

# The command Docker runs to launch the service application.
CMD ["python", "api.py"]