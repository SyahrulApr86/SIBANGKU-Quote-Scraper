# Gunakan image Python sebagai base
FROM python:3.9-slim

# Copy seluruh file ke dalam container
WORKDIR /app
COPY . /app

# Install dependencies dari requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 untuk Flask
EXPOSE 5000

# Jalankan aplikasi Flask
CMD ["python", "app.py"]
