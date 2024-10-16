# Gunakan image Python sebagai base
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Copy seluruh file ke dalam container
WORKDIR /app
COPY . /app

# Install dependencies dari requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# Jalankan script secara langsung
CMD ["python", "script.py"]
