from __future__ import absolute_import

from docker.celery import app
from celery import shared_task


@shared_task
def print_hello(data):
    print("hello")