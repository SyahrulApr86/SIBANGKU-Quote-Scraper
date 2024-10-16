# Gunakan image Python sebagai base
FROM python:3.9-slim

# Install cron
RUN apt-get update && apt-get install -y cron

# Copy script dan file dependencies ke dalam container
WORKDIR /app
COPY . /app

# Install dependencies dari requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy crontab file
COPY crontab /etc/cron.d/my-cron-job

# Beri izin pada crontab file
RUN chmod 0644 /etc/cron.d/my-cron-job

# Apply crontab file
RUN crontab /etc/cron.d/my-cron-job

# Start cron service dan jalankan container
CMD ["cron", "-f"]
