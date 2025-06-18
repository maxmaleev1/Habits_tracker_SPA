# Используем минимальный Python-образ
FROM python:3.10-slim

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry==1.7.1

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем зависимости
COPY pyproject.toml poetry.lock* ./

# Устанавливаем зависимости без dev
RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi

# Копируем весь проект
COPY . .

# Открываем порт (если будет использоваться)
EXPOSE 8000

# Команда запуска
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
