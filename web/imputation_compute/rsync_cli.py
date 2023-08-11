#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: soliva
@Site:
@file: python_pipe_temp.py
@time: 2022/11/23
@desc:
'''
## celery import as RabbitMQ
from __future__ import absolute_import
from celery import Celery

app = Celery('test_celery',
broker='amqp://test:test123@localhost/test_vhost',
backend='rpc://',
include=['test_celery.tasks'])


