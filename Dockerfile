# Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Systémové závislosti (minimální)
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

# Zkopíruj requirementy a nainstaluj
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Zkopíruj zbytek aplikace
COPY . /app/

EXPOSE 3000

# Výchozí příkaz spustí Gunicorn na portu 8080
CMD ["gunicorn", "main.wsgi:application", "--bind", "0.0.0.0:3080", "--workers", "3"]