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
## Скриншоты
### Главная страница
![image](https://user-images.githubusercontent.com/38291314/179191052-6a08a0bb-61f2-4648-a2d3-c6f17240ea47.png)
### Список рецептов
![image](https://user-images.githubusercontent.com/38291314/179192845-3a4d60b3-cb96-468a-b45e-6c9140361ec6.png)
![image](https://user-images.githubusercontent.com/38291314/179192913-149f0b3e-00de-4feb-a0be-594170357b71.png)
### Просмотр рецепта
![image](https://user-images.githubusercontent.com/38291314/179178539-af7dc5eb-5f46-4646-aa99-3c6f934e96b7.png)
### Комментарии рецепта
![image](https://user-images.githubusercontent.com/38291314/179181741-c2a0699c-33af-4459-bc97-0424816c63bd.png)
### Первоначальное создание рецепта
![image](https://user-images.githubusercontent.com/38291314/179179484-34272606-5187-488a-a33e-8be8609be95e.png)
### Редактирование рецепта
1
![image](https://user-images.githubusercontent.com/38291314/179178734-c301ad1f-0901-4aae-99bd-681dd0b6b816.png)
2
![image](https://user-images.githubusercontent.com/38291314/179178779-e75fd49a-ae3b-4510-950f-d1910a81ee88.png)
### Регистрация
![image](https://user-images.githubusercontent.com/38291314/179180688-204a32e5-3f41-486d-8b3b-e754e656095a.png)
### Логин
![image](https://user-images.githubusercontent.com/38291314/179180922-a69c9c8c-54c1-4dda-a2f8-fbaa934446a6.png)
### Информация о пользователе
![image](https://user-images.githubusercontent.com/38291314/179180029-56eff76f-415d-4e59-b075-69693078fd7c.png)
![image](https://user-images.githubusercontent.com/38291314/179180162-af7cc984-15da-43b9-b5f6-a47a85115f98.png)
### Редактирование информации о пользователе
1
![image](https://user-images.githubusercontent.com/38291314/179179661-7e3a9064-2f35-4c10-be29-1a6365ebebac.png)
2
![image](https://user-images.githubusercontent.com/38291314/179179816-119bb757-b81a-4978-8f08-15ebf3cfb274.png)
### Форма обратной связи
![image](https://user-images.githubusercontent.com/38291314/179182112-fb8678b1-3fef-41d2-8183-680eec048011.png)
