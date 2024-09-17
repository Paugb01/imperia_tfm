# Dockerfile for Streamlit UI
FROM python:3.9-slim

# Create and set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
COPY image.png /app/
COPY pakotinaikos-5b1bb10e7834.json /app/credentials-file.json  
COPY ui.py /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the Google Cloud credentials environment variable
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/credentials-file.json"

# Expose the port the app runs on
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "ui.py", "--server.port=8501", "--server.address=0.0.0.0"]
