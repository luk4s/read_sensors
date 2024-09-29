FROM python:3.13.0rc2-slim
LABEL org.opencontainers.image.authors="Lukas Pokorny <admin@luk4s.cz>"
LABEL org.opencontainers.image.source="https://github.com/luk4s/read_sensors"
LABEL org.opencontainers.image.licenses="MIT"
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["./docker-entrypoint.sh"]