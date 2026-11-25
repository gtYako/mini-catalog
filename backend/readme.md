# Mini-Catalog: Каталог услуг учебного центра

##  Стек технологий
* Python 3.x
* Django (и Django REST Framework)
* django-filter (фильтрация)
* django-cors-headers (поддержка CORS для будущего React-фронтенда)
* SQLite (база данных)

##  Инструкция по запуску (с нуля)

Для запуска проекта понадобятся установленный Python и Git.

### 1. Клонирование репозитория и переход в папку
```bash
git clone <ссылка_на_твой_репозиторий>
cd mini-catalog
### 2. Создание и активация виртуального окружения
Для Windows:

bash
python -m venv .venv
.venv\Scripts\activate
Для macOS / Linux:

bash
python3 -m venv .venv
source .venv/bin/activate
 
 3. Установка зависимостей
Все необходимые библиотеки описаны в requirements.txt.

bash
pip install -r requirements.txt
4. Настройка переменных окружения (Секретный ключ)
Секретный ключ хранится вне репозитория. Вам нужно создать файл .env в папке backend/ (рядом с manage.py).
Создайте файл backend/.env и добавьте в него:

env
DJANGO_SECRET_KEY=придумайте_любой_длинный_секретный_ключ
DJANGO_DEBUG=1
(Для генерации ключа можно использовать команду python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")

5. Применение миграций (создание базы данных)
Перейдите в папку backend:

bash
cd backend
Примените миграции для создания таблиц:

bash
python manage.py migrate
6. Наполнение базы тестовыми данными (Seed)
Проект содержит кастомную команду для автоматического создания 4 категорий, 15 услуг и 8 заявок:

bash
python manage.py seed_data
7. Создание администратора (Superuser)
Чтобы зайти в панель администратора и управлять услугами:

bash
python manage.py createsuperuser
(Введите логин, email и пароль).

8. Запуск сервера
bash
python manage.py runserver
Сервер будет доступен по адресу: http://127.0.0.1:8000/