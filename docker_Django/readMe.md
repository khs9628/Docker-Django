# Docker - Nginx - gunicorn - Django 구축하기

Django서버의 기본구조인 Nginx/gunicorn/Django 구조를 Docker-compose를 통해 구성해보겠습니다.

### 폴더 구조
    [docker]
    ├─app  *django app
    ├─docker *django project
    ├─media *django media
    ├─static *django static 
    └─nginx *nginx config 

[사진](/url)

### Django 프로젝트 세팅
기본 프로젝트 세팅은 생략하겠습니다. (git주소의 프로젝트 파일 참고)


### 기본 Dockfile 구성
```
# docker/DockFile

FROM python:3.7 

RUN apt-get -y update

RUN mkdir /srv/test
COPY requirements.txt /srv/test/

WORKDIR /srv/test

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /srv/test/

```


### Nginx DockFile 구성
```
# /docker/nginx/DockFile

FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d


# /docker/nginx/nginx.conf

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

### Nginx와 Gunicorn을 묶어줄 docker-compose파일 구성
```
# /docker/docker-compose.yml

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
      - .:/srv/test
      - ./log:/var/log/docker
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
      - .:/srv/test
      - ./nginx:/etc/nginx/conf.d
    ports:
      - "80:80"
    depends_on:
      - app

```

### docker-compose 파일 실행

```
$ docker-compose build
$ docker-compose up 

# 두 명령어 한번에
$ docker-compose up --build
```