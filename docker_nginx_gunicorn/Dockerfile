FROM python:3.7 

RUN apt-get -y update

RUN mkdir /srv/test
COPY requirements.txt /srv/test/

WORKDIR /srv/test

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /srv/test/
