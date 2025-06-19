FROM python:3.10-slim

# Устанавливаем системные зависимости: компиляторы и PostgreSQL
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN pip install --no-cache-dir "poetry==1.6.1"

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED=1

# Создаём директорию приложения
WORKDIR /app

# Копируем проект целиком
COPY . .

# Отключаем виртуальные окружения и устанавливаем зависимости (только main)
RUN poetry config virtualenvs.create false \
  && poetry install --only main --no-interaction --no-ansi


# Открываем порт и запускаем приложение через Gunicorn
EXPOSE 8000
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
