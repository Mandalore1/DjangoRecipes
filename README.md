# DjangoRecipes
## Описание
Сайт рецептов
## Стек
* Python 3.10
* Django 4.0.5
* SQLite3 / PostgreSQL
* Плагины Django: Debug Toolbar, Ckeditor, Environ
* Bootstrap 5.2
## Запуск
### Настройка переменных окружения
В папке Recipes создать файл переменных окружения .env.

Для возможности отправки писем обратной связи, указать данные почтового сервера и почтового ящика:
```
EMAIL_HOST=
EMAIL_HOST_PASSWORD=
EMAIL_HOST_USER=
```
Если будет использоваться база данных PostgreSQL, указать следующие данные:
```
DATABASE_NAME=
DATABASE_USER=
DATABASE_PASSWORD=
DATABASE_HOST=
DATABASE_PORT=
```
### Установка зависимостей
Установить зависимости
```bash
pip install -r requirements.txt
```
### Настройка базы данных
В файле Recipes/settings.py в настройке DATABASES раскомментировать строки, относящиеся к используемой базе данных (SQLite3 или PostgreSQL) и закомментировать строки другой базы данных.

Сделать миграции
```bash
python manage.py makemigrations
python manage.py migrate
```
### Статические файлы
Скачать и разархивировать библиотеки в каталог Recipes/static/libs: https://drive.google.com/file/d/1mV6W4xatTi22DvJd-y17kIpZ0h0CzqM-/view?usp=sharing

Собрать статические файлы
```bash
python manage.py collectstatic
```
### Запуск
Запустить с помощью
```bash
python manage.py runserver
```
## Возможности
* Рецепты
  * Добавление, изменение, удаление и просмотр рецептов
  * Поиск рецептов по названию и пользователю
  * Сортировка рецептов по дате, алфавиту и просмотрам
  * Добавление рецепта в избранное
  * Комментирование рецептов
* Пользователи
  * Регистрация и логин
  * Профиль пользователя
  * Форма обратной связи
