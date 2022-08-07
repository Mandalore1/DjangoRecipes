# Запуск в Docker
## Начало
1. Скачать и разархивировать библиотеки в каталог Recipes/static/libs: 
https://drive.google.com/file/d/1mV6W4xatTi22DvJd-y17kIpZ0h0CzqM-/view?usp=sharing
2. В файле Recipes/settings.py в настройке DATABASES раскомментировать строки, относящиеся к PostgreSQL и закомментировать строки другой базы данных.
## Запуск в режиме debug
1. В папке Recipes создать файл переменных окружения .env на основе .env_template. Указать DEBUG=1.
2. Запустите docker-compose
```bash
docker-compose build
docker-compose up -d
docker-compose exec web python manage.py migrate --noinput
```
## Запуск в режиме production
1. Из папки prod перенести все и заменить в корневой папке
2. В папке Recipes создать файл переменных окружения .env на основе .env_template. Указать DEBUG=0.
3. В settings.py указать ALLOWED_HOSTS (например, ['localhost', '127.0.0.1', '[::1]'])
3. В settings.py указать CSRF_TRUSTED_ORIGINS (например, ['https://localhost/', 'https://127.0.0.1/', 'https://[::1]/'])
4. Запустите docker-compose
```bash
docker-compose build
docker-compose up -d
docker-compose exec web python manage.py migrate --noinput
```