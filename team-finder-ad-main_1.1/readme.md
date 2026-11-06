# TeamFinder - Социальная сеть для программистов (Вариант 1)

## Функциональность
Регистрация и вход по email, создание/редактирование/завершение проектов, добавление в избранное, участие в проектах, фильтрация пользователей по 4 критериям, редактирование профиля, смена пароля, админ-панель, пагинация (12 элементов).

## Технологии
Python 3.12, Django 5.2.4, SQLite/PostgreSQL, Docker.

## Установка и запуск

cd "Папка с проектом"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env_example .env
python manage.py makemigrations users
python manage.py makemigrations projects
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

## Если PostgreSQL не работает
В файле team_finder/settings.py замените DATABASES на: DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}}

## Если ошибка "no such table"
del db.sqlite3
rmdir /s /q users\migrations
rmdir /s /q projects\migrations
python manage.py makemigrations users
python manage.py makemigrations projects
python manage.py migrate

## Остановка проекта
Ctrl + C, затем deactivate

## Тестовые данные
admin@example.com / admin123
test@test.com / test123

## Основные URL
Главная: http://127.0.0.1:8000
Админка: http://127.0.0.1:8000/admin
Регистрация: http://127.0.0.1:8000/users/register
Вход: http://127.0.0.1:8000/users/login
Список пользователей: http://127.0.0.1:8000/users/list
Создание проекта: http://127.0.0.1:8000/projects/create-project
Избранное: http://127.0.0.1:8000/projects/favorites

## Автор
Дипломный проект. Вариант №1 (Избранное и фильтрация пользователей)