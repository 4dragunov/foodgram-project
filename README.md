#
![Build Status](https://github.com/4dragunov/foodgram-project/workflows/foodgram-workflow/badge.svg)

# Описание проекта
Проект продуктовый помощник Foodgram
. <br>Это онлайн-сервис, где пользователи смогут публиковать рецепты, 
подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.
<br><br>Проект доступен по адресу: http://178.154.204.140 <br><br>
Тестовый пользователь <br>
test,
admin123q


В корне проекта файл `entrypoint.sh` собирает статику и выполняет миграции. 

## Установка на локальном компьютере
Приведенная ниже последовательность позволит развернуть проект на локальной машине для тестирования
### Установка Docker
Для запуска проекта необходима установка программ `docker` и `docker-compose`. https://docs.docker.com/engine/install/
### Запуск проекта (Lunux)  
1. Создайте на локальном ПК папку проекта foodgram-project командой `mkdir
 foodgram-project`
 
2. Склонируйте репозиторий в текущую папку командой 
`git clone https://github.com/4dragunov/ foodgram-project/ .` и перейдите в нее командой `cd  foodgram-project`

3. Создайте файл `.env` командой `touch .env
` с переменными окружениями для работы с базой данных на основе шаблона
 для работы с базой данных:
 ```
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД 
```
3.Измените файл конфигурации `.github/workflows/main.yml` закоментируйте строку 

4.Запустите `docker-compose` командой sudo `docker-compose up -d`

Следующие шаги выполняет скрипт `entrypoint.sh`, в случае ручного выполнения необходимо выполнить следующие команды

- Создайте миграции `sudo docker-compose exec web python manage.py migrate`

- Соберите статику проекта командой `sudo docker-compose exec web python
 manage.py collectstatic --no-input`

5.Создайте суперпользователя Django `sudo docker-compose exec web python
 manage.py createsuperuser`

6.Загрузите фикстуры (тестовые данные) в базу данных командой `sudo docker
-compose exec web python manage.py loaddata fixtures.json`


После описанных выше действий проект будет доступен по адресу `http://127.0.0.1`

## Установка (деплой) на удаленном сервере
## Деплой с использованием git actions
Необходимо создать переменные окружения в вашем репозитории github
 в разделе `secrets`
```
DOCKER_PASSWORD # Пароль от Docker Hub
DOCKER_USERNAME # Логин от Docker Hub
HOST # Публичный ip адрес сервера
USER # Пользователь сервера
PASSPHRASE # Если ssh-ключ защищен фразой-паролем
SSH_KEY # Приватный ssh-ключ
```
При каждом деплое будет происходить:
- сборка и обновление образа на сервисе `docker-hub`
- автоматический деплой на сервер, указанный в `secrets`
При необходимости изменения или добавления действий редактируйте файл `.github/workflows/main.yml`. <br>

### Использованные технологии
Django Rest Framework https://www.django-rest-framework.org/ <br>
Django https://www.djangoproject.com/ <br>
PostgreSQL https://www.postgresql.org/ <br>
Docker https://www.docker.com/ <br>

### Авторы проекта
Алексей Драгунов - Python Developer <br>

### Лицензии
Этот проект, включая все файлы и их содержимое, лицензирован в соответствии с условиями лицензии MIT.<br>
Смотрите LICENSE.txt для деталей.


