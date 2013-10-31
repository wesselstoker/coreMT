#!bin/python

import sys
from random import choice

from celery import Celery

import yajl as json
import toml

import xmlrpc.client
import requests

## Load config file
with open("config/worker.toml") as config_file:
    config = toml.loads(config_file.read())

## Celery configuration
celery = Celery('tasks', backend=config["queue"]["backend"], broker=config["queue"]["broker"])
celery.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
)


@celery.task
def translate(text, language):
    ## Choose random server from the server list.
    ## TODO: Make this less ugly :)
    result = json.loads(requests.get("http://localhost:4001/v1/keys/language:{0}".format(language)).text)
    server = choice(json.loads(result["value"])["servers"])

    proxy = xmlrpc.client.ServerProxy(server)
    try:
        translation = proxy.translate({"text":text.lower()})
    except Exception as err:
        return err

    return json.dumps(translation)


@celery.task
def log_message(timestamp, message):
    return "blub"

if __name__ == '__main__':
    celery.start()
