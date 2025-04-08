# Система бронирования столов в ресторане

API для управления бронированием столов в ресторане, разработанное с использованием **FastAPI** и **PostgreSQL**. Система включает функции для управления столами, бронированиями и предотвращения конфликтов.

## Основные функции
- **Управление столами**: добавление, удаление, просмотр.
- **Бронирование**: создание и отмена бронирований.
- **Проверка доступности**: предотвращение конфликтов бронирований.
- **Асинхронный доступ к базе данных**.
- **Контейнеризация с Docker**.
- **Миграции базы данных** с Alembic.

## Технологии
- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy**
- **Alembic**
- **Docker & Docker Compose**
- **Pydantic**
- **Pytest**

## Запуск проекта

### Требования
- Docker
- Docker Compose

### Шаги для запуска
Клонируйте репозиторий:

   ```bash
   git clone https://github.com/EVA666999/restaurant_reservations/
   cd app
   ```
## Создайте файл .env с переменными:
POSTGRES_DB=test_case_db_1
POSTGRES_USER=postgres
POSTGRES_PASSWORD=ваш_пароль
DB_HOST=postgres
DB_PORT=5432
##Для миграций выполните:
alembic init alembic
##Настройте alembic.sqlalchemy.url = postgresql://postgres:password@localhost:5432/name_db
ini:
##Примените миграции:
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
##Запустите приложение с Docker:
docker compose up --build
##API будет доступно по адресу:
http://localhost:8000

##Особенности

Поддержка различных расположений столов.
Автоматическая проверка конфликта бронирований.
Уведомление о ближайшем доступном времени при отказе в бронировании.
Тестирование с Pytest.



