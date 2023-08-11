#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: soliva
@Site: 
@file: custumerRsyncSingleQueue.py
@time: 2023/7/5
@desc:
'''
import asyncio
import subprocess
import pika
import json
### https://github.com/scrapy/queuelib
###is a disk queues  queue library
from queuelib import FifoDiskQueue

from redis_queue import Queue
import config as c

redis_host = c.redishost
redis_port = c.redisport
redis_password = c.redispassword
rabbitmq_host = c.rabbitmqhost#"192.168.77.45"#
rabbitmq_port = c.rabbitmqport
rabbitmq_username = c.rabbitmqusername#"guest" #
rabbitmq_password = c.rabbitmqpassword#"guest"#
rabbitmq_exechange = c.rabbitmqexechange



import pika
import uuid

class Consumer:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host,5672, '/', pika.PlainCredentials(rabbitmq_username,rabbitmq_password)))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=rabbitmq_exechange, exchange_type='fanout')

        self.queue_name = self.channel.queue_declare(queue='', exclusive=True).method.queue
        self.channel.queue_bind(exchange=rabbitmq_exechange, queue=self.queue_name)

        self.seen_messages = set()  # 记录已处理的消息标识符

    def handle_message(self, ch, method, properties, body):
        message_id = properties.message_id

        # 检查消息标识符是否已存在，避免重复处理
        if message_id in self.seen_messages:
            print(f"Skipping duplicate message: {message_id}")
            return

        print(f"Received {message_id} message: {body}")
        message = body

        ### using redis queue Persistence queue
        q = Queue("queueRsync", host=redis_host, port=redis_port, password=redis_password)
        message_json = json.loads(message)
        message_json["local"]=c.local
        message = json.dumps(message_json)
        send_queue = q.put_nowait(message)
        # 在这里处理消息的逻辑

        # 记录已处理的消息标识符
        self.seen_messages.add(message_id)

        # 发送消息确认
        self.channel.basic_ack(delivery_tag=method.delivery_tag)

    def start_consuming(self):
        # 设置消息消费者，设置prefetch_count限制并发连接数
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.handle_message)

        print('Waiting for messages...')
        self.channel.start_consuming()

    def close_connection(self):
        self.connection.close()

if __name__ == '__main__':
    consumer = Consumer()
    try:
        consumer.start_consuming()
    except KeyboardInterrupt:
        consumer.close_connection()




