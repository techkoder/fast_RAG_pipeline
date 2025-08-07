# Use official Python 3.11 image for Hugging Face Spaces compatibility
FROM python:3.11

# Set working directory
WORKDIR /code

# Copy project files into container
COPY . /code

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --upgrade -r requirements.txt

# Expose port 7860 for Hugging Face Spaces
EXPOSE 7860

# Start FastAPI using Uvicorn on the expected port
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "7860"]
