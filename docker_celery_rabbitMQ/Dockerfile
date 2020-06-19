FROM python:3.7 

RUN apt-get -y update
RUN mkdir /srv/plugin
COPY requirements.txt /srv/plugin/

WORKDIR /srv/plugin

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /srv/plugin/
