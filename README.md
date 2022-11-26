# Проект Foodgram
![workflow](https://github.com/Yuliya0506/foodgram-project-react/actions/workflows/main.yml/badge.svg?)

Foodgram - продуктовый помощник с базой кулинарных рецептов. 
Позволяет публиковать рецепты, сохранять избранные, а также формировать список покупок для выбранных рецептов.
Можно подписываться на любимых авторов.


Проект доступен по [адресу](http://51.250.91.217/recipes)

Документация к API доступна [здесь](http://51.250.91.217/api/docs/)


## Запуск проекта

* Для работы с GitHub Actions необходимо в репозитории в разделе Secrets > Actions создать переменные окружения:
````
SECRET_KEY              # секретный ключ Django проекта
DOCKER_PASSWORD         # пароль от Docker Hub
DOCKER_USERNAME         # логин Docker Hub
HOST                    # публичный IP сервера
USER                    # имя пользователя на сервере
PASSPHRASE              # *если ssh-ключ защищен паролем
SSH_KEY                 # приватный ssh-ключ
TELEGRAM_TO             # ID телеграм-аккаунта для посылки сообщения
TELEGRAM_TOKEN          # токен бота, посылающего сообщение

DB_ENGINE               # django.db.backends.postgresql
DB_NAME                 # postgres
POSTGRES_USER           # postgres
POSTGRES_PASSWORD       # postgres1
DB_HOST                 # db
DB_PORT                 # 5432 (порт по умолчанию)
````

* Клонировать репозиторий:
````
git clone git@github.com:Yuliya0506/foodgram-project-react.git
````

* Подключаемся к серверу
````
ssh <server user>@<public server IP>
````

* Устанавливаем докер
````
sudo apt install docker.io
````

* Устанавливаем Docker-Compose (для Linux)
````
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
````

* Получаем права для docker-compose
````
sudo chmod +x /usr/local/bin/docker-compose
````

* Загружаем файлы docker-compose.yaml и nginx.conf на сервер, сделать это можно командой (в случае удаленного запуска)
````
scp docker-compose.yaml <username>@<public ip adress>:/home/<username>/docker-compose.yaml
````


### В проекте использованы технологии:
- Python
- Django
- Django REST Framework
- Docker
- PostgreSQL
- Gunicorn
- Nginx
- Yandex Cloud

### Проект выполнила студентка 37 когорты Яндекс Практикума:
Юлия Галиева     https://github.com/Yuliya0506
