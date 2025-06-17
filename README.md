# Habits Tracker SPA

Это Single Page Application (SPA) для отслеживания привычек, разработанное на Django с поддержкой Telegram-напоминаний. Проект контейнеризирован с использованием Docker и автоматизирован через GitHub Actions (CI/CD).

---

## 🌐 Продакшн-версия

Приложение развернуто на удаленном сервере и доступно по адресу:

**http://89.169.166.102**

---

## 📦 Функциональность

- Отслеживание привычек
- Напоминания через Telegram-бота
- REST API с JWT-аутентификацией
- Админ-панель
- CI/CD через GitHub Actions

---

## 🚀 Локальный запуск

### 📋 Предварительные требования

- Docker
- Docker Compose
- Git

### ⚙️ Шаги

```bash
# 1. Клонируем репозиторий
git clone https://github.com/maxmaleev1/Habits_tracker_SPA.git
cd Habits_tracker_SPA

# 2. Копируем переменные окружения
cp .env.sample .env

# 3. Собираем и запускаем контейнеры
docker-compose up --build
```

Теперь приложение будет доступно по адресу: [http://localhost:8000](http://localhost:8000)

---

## ☁️ Развертывание на удалённый сервер

### Шаги настройки сервера

1. Установите на сервер:
   - Docker
   - Docker Compose

2. Клонируйте проект:
   ```bash
   git clone https://github.com/maxmaleev1/Habits_tracker_SPA.git
   cd Habits_tracker_SPA
   ```

3. Настройте `.env`:
   ```bash
   cp .env.sample .env
   ```

4. Убедитесь, что открыт порт `80` и `docker-compose.yml` находится в корне проекта.

5. Добавьте SSH-ключ в GitHub Secrets (`SSH_PRIVATE_KEY`)

6. GitHub Actions автоматически выполнит:
   - `git pull`
   - `docker-compose pull`
   - `docker-compose up -d --remove-orphans`

---

## 🔁 CI/CD через GitHub Actions

Файл CI/CD: `.github/workflows/ci.yml`

### Этапы:

1. **Lint** — проверка кода `flake8`
2. **Test** — выполнение `manage.py test` с PostgreSQL
3. **Build** — сборка Docker-образа
4. **Push** — отправка образа в Docker Hub
5. **Deploy** — деплой на сервер через SSH и `docker-compose`

### Секреты, необходимые в GitHub Secrets:

| Название               | Описание                        |
|------------------------|----------------------------------|
| `DJANGO_SECRET_KEY`    | Секретный ключ Django            |
| `POSTGRES_DB`          | Имя базы данных                  |
| `POSTGRES_USER`        | Пользователь PostgreSQL          |
| `POSTGRES_PASSWORD`    | Пароль PostgreSQL                |
| `POSTGRES_HOST`        | Хост базы данных                 |
| `POSTGRES_PORT`        | Порт PostgreSQL (обычно 5432)    |
| `DOCKER_HUB_USERNAME`  | Имя пользователя Docker Hub      |
| `DOCKER_HUB_TOKEN`     | Токен доступа Docker Hub         |
| `SSH_PRIVATE_KEY`      | SSH-ключ для доступа к серверу   |
| `SSH_USER`             | Логин на сервере                 |
| `SERVER_IP`            | IP-адрес сервера (89.169.166.102)|

---

## 📂 Структура проекта

```
Habits_tracker_SPA/
├── config/                # Настройки Django
├── habits/                # Модуль привычек
├── users/                 # Аутентификация пользователей
├── telegram_reminder/     # Telegram-напоминания
├── nginx/                 # Конфигурация nginx
├── .github/workflows/     # GitHub Actions workflow
├── Dockerfile             # Docker-образ приложения
├── docker-compose.yml     # Compose-файл для запуска
├── .env.sample            # Пример переменных окружения
```

---

## 🧪 Тестирование

Запуск тестов локально:

```bash
docker-compose exec web python manage.py test
```

---

## 📬 Контакты

- **Автор:** [maxmaleev1](https://github.com/maxmaleev1)
- **Проект:** https://github.com/maxmaleev1/Habits_tracker_SPA