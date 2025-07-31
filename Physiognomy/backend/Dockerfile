# Dockerfile

# 1. Base image
FROM python:3.9

# 2. Install OS dependencies for OpenCV
RUN apt-get update && apt-get install -y libgl1-mesa-glx

# 3. Set working directory
WORKDIR /app

# 4. Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy application code
COPY . .

# 6. Expose port and run application
EXPOSE 8001
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]