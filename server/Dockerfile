# Use official slim Python image (small and fast)
FROM python:3.13-slim

# Set working directory inside the container
WORKDIR /app

# Copy the entire project into the container
COPY . .

# Optional: Install dependencies (add to requirements.txt if needed)
RUN pip install --no-cache-dir -r requirements.txt || true

# Default command to run the modular server
CMD ["python", "main.py"]
