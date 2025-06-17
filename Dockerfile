FROM python:3.10-slim

# Устанавливаем Poetry
RUN pip install --no-cache-dir "poetry==1.6.1"

# Создаём директорию приложенияя
WORKDIR /app

# Копируем весь проект сразу (в том числе папки с кодом)
COPY . .

# Отключаем виртуальные окружения и устанавливаем зависимости (только main)
RUN poetry config virtualenvs.create false \
  && poetry install --only main --no-interaction --no-ansi

# Открываем порт и задаём команду по умолчанию
EXPOSE 8000
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
