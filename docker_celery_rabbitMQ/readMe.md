# Docker - Celery - rabbitMQ - Django 구축하기

Django서버의 비동기서버인 Celery와 Celery의 Worker(task)를 제어하는
Celery - rabbitMQ - Django 구조를 Docker로 구축하겠습니다.

### 폴더 구조
    [docker_celery_rabbitMQ]
    ├─app  *django app
    ├─docker *django project
    ├─media *django media
    ├─static *django static 
    └─nginx *nginx config 

`자세한 구조는 git 폴더를 참고하세요`

[사진](/url)

### Django 프로젝트 세팅

1. app 파일 수정
```
# /app/tasks.py
from __future__ import absolute_import

from docker.celery import app
from celery import shared_task


@shared_task
def print_hello():
    print("hello")

# /app/views.py
from django.shortcuts import render
from django.http import HttpResponse

from .tasks import *

def print_celery(reqeust):
    print_hello.delay()
    return HttpResponse("Hello, world. Celery_RabbitMQ_Clear")

# /app/urls.py
from django.urls import path, include
from . import views


urlpatterns = [
    path('print_celery/', views.print_celery, name='print_celery'),
]

```

2. 프로젝트 파일 수정
```
# /docker/__init__.py
from __future__ import absolute_import, unicode_literals
from .celery import app as celery_app

__version__ = '1.0'

__all__ = ['celery_app']


# /docker/celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from datetime import timedelta
from celery.schedules import crontab

from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'docker.settings')

app = Celery('docker', broker='amqp://admin:1234@rabbit:5672//')

# v4.0 이상 일 경우
app.config_from_object('django.conf:settings', namespace='CELERY')
# v3.1 일 경우
# app.config_from_object('django.conf:settings')

# v4.0 이상 일 경우
app.autodiscover_tasks()
# v3.1 일 경우
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],  # Ignore other content
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TIMEZONE='Asia/Seoul',
    CELERY_ENABLE_UTC=False,
    CELERYBEAT_SCHEDULE = {
        'say_hello': {
            "task": "app.tasks.print_hello",
            'schedule': crontab(minute=0, hour=5),
            'args': ()
        },
    }
)

```


### 기본 Dockfile 구성
```
# ./DockerFile

FROM python:3.7 

RUN apt-get -y update

RUN mkdir /srv/celery
COPY requirements.txt /srv/celery/

WORKDIR /srv/celery

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /srv/celery/


```


### Nginx DockFile 구성
```
# /nginx/DockerFile

FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d


# /nginx/nginx.conf

upstream django {
    server app:8000;
}

server {
    listen 80;
    server_name localhost;
    
    location / {
        try_files $uri @proxy_to_app;
    }

    location @proxy_to_app {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Host $server_name;
    }

    location /media/ {
        alias /srv/docker/media/;
    }

    location /static/ {
        alias /srv/docker/static/;
    }
}

```

### 전체 설정정보가 담긴 docker-compose파일 구성
```
# ./docker-compose.yml

version: '3'
services:
  app:
    build:  
      context: .
      dockerfile: Dockerfile 

    container_name: django
    restart: always
    ports:
      - "8000:8000"    
    volumes:
      - .:/srv/celery
      - ./log:/var/log/celery
    command: 
      gunicorn --workers=2 --bind 0.0.0.0:8000 docker.wsgi:application
      
    expose: 
      - "8000"

  nginx:
    container_name: nginx
    build: 
      context: ./nginx
      dockerfile: Dockerfile 
    restart: always
    volumes:
      - .:/srv/celery
      - ./nginx:/etc/nginx/conf.d
    ports:
      - "80:80"
    depends_on:
      - app


  rabbit:
    container_name: rabbit
    hostname: rabbit
    image: rabbitmq:latest
    environment:
      - RABBITMQ_DEFAULT_USER=admin
      - RABBITMQ_DEFAULT_PASS=1234
    ports:
      - "5672:5672"

  worker:
    container_name: celery
    build: .
    volumes:
      - .:/srv/celery
    environment:
      - C_FORCE_ROOT=true
    command: 
      celery -A docker worker -l info
    links:
      - rabbit
    depends_on:
      - rabbit
  
  celery-beat:
    container_name: celery-beat
    build: .
    command: celery -A docker beat -l info
    volumes:
      - .:/srv/celery
    links:
      - rabbit
    depends_on:
      - rabbit

```

### docker-compose 파일 실행

```
$ docker-compose build
$ docker-compose up 

# 두 명령어 한번에
$ docker-compose up --build
```