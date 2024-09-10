# Dockerfile for FastAPI app
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI app and other necessary files
COPY app2.py .
COPY xgb_model_v3.pkl .
COPY scaler_v3.pkl .
COPY ordinal_encoder_v3.pkl .

# Expose the port the app runs on
EXPOSE 8000

# Run the FastAPI app
CMD ["uvicorn", "app2:app", "--host", "0.0.0.0", "--port", "8000"]
