FROM python:3.12-slim
LABEL maintainer="Lukas Pokorny <admin@luk4s.cz>"
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["./docker-entrypoint.sh"]