# Online server (VPS) par 24 kalak chalavva: docker compose up -d
FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg libraqm0 tzdata && rm -rf /var/lib/apt/lists/*
ENV TZ=Asia/Kolkata PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["python", "main.py", "--app", "--server", "--port", "8080"]
