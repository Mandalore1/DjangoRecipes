FROM python:3.10-alpine

# Устанавливаем некоторые переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем директорию с приложением
WORKDIR /usr/src/django-recipes

# Копируем файлы в директорию
COPY . .

# Устанавливаем необходимые библиотеки для psycopg2
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# Устанавливаем необходимые зависимости
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Собираем статические файлы
RUN python manage.py collectstatic
