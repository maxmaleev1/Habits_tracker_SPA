# Используем официальный образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry==1.7.1

# Копируем файлы зависимостей в контейнер
COPY pyproject.toml poetry.lock* ./

# Отключаем создание виртуального окружения и устанавливаем только основные зависимости
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --only main --no-interaction --no-ansi

# Копируем оставшиеся файлы проекта
COPY . .

# Команда по умолчанию при запуске контейнера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

