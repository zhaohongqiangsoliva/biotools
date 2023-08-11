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

from models.task import Task
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from tortoise import Tortoise, run_async
import aiomysql

### https://github.com/scrapy/queuelib
###is a disk queues  queue library
#from queuelib import FifoDiskQueue

#from redis_queue import Queue
import config as  c
c.rabbitmqhost='118.195.223.193'
c.rabbitmqport=5672
c.rabbitmqusername='prs_hub'
c.rabbitmqpassword='zcygkc36'



rabbitmq_host = c.rabbitmqhost#"192.168.77.45"#
rabbitmq_port = c.rabbitmqport
rabbitmq_username = c.rabbitmqusername#"guest" #
rabbitmq_password = c.rabbitmqpassword#"guest"#


# def callback(ch, method, properties, body):
#     # 将接收到的消息解析为任务信息
#     message  = body
#     print(message)
#
#     ### using redis queue Persistence queue
#     q = Queue("queueRsync", host=redis_host, port=redis_port, password=redis_password)
#     send_queue = q.put_nowait(message)
#     # if send_queue == True:
#     #     ch.basic_ack(delivery_tag=method.delivery_tag)
#
#     # 执行任务
#     print("message" ,"alrady join to qeueue")
#
#
#
# connection = pika.BlockingConnection(
#     pika.ConnectionParameters(rabbitmq_host,5672, '/', pika.PlainCredentials(rabbitmq_username,rabbitmq_password)))
#     #pika.ConnectionParameters('192.168.77.45',5672, '/', pika.PlainCredentials('guest','guest')))
# channel = connection.channel()
#
# # result = channel.queue_declare(queue='', exclusive=True)
# # queue_name_2 = result.method.queue
# # channel.queue_bind(exchange='my_exchange', queue=queue_name_2)
# # # 声明队列
# # # channel.queue_declare(queue='task_queue')
# # channel.basic_consume(queue=queue_name_2, on_message_callback=callback, auto_ack=False)
# # 消费者订阅队列，并指定回调函数处理消息
#
#
# #channel.queue_declare(queue='imputation.upload.file.queue.shanghai',durable=True)
# channel.basic_consume(queue='imputation.upload.file.queue.beijing', on_message_callback=callback, auto_ack=True)
# print(' [*] Waiting for messages. To exit press CTRL+C')
# # 启动消费者循环，持续等待任务到达并处理
# channel.start_consuming()


import pika
import uuid


async def save_or_update_task(mysqlSaveDict):
    job_id = mysqlSaveDict['jobID']
    # 尝试获取具有相同jobID的任务
    existing_task = await Task.get_or_none(jobID=job_id)

    if existing_task:
        # 如果存在相同jobID的任务，则更新现有记录
        await Task.filter(jobID=job_id).update(**mysqlSaveDict)
    else:
        # 如果不存在相同jobID的任务，则创建新记录
        await Task.create(**mysqlSaveDict)


class Consumer:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host,5672, '/', pika.PlainCredentials(rabbitmq_username,rabbitmq_password)))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange="exange_QUEUE_UUID", exchange_type='fanout')

        self.queue_name = self.channel.queue_declare(queue='', exclusive=True).method.queue
        self.channel.queue_bind(exchange="exange_QUEUE_UUID", queue=self.queue_name)

        self.seen_messages = set()  # 记录已处理的消息标识符

    def handle_message(self, ch, method, properties, body):
        message_id = properties.message_id

        # 检查消息标识符是否已存在，避免重复处理  此消息produce提供
        if message_id in self.seen_messages and message_id:
            print(f"Skipping duplicate message: {message_id}")
            return

        print(f"Received {message_id} message: {body}")
        message = body

        ### using redis queue Persistence queue
        message_json = json.loads(message)
        Task_Pydantic = pydantic_model_creator(Task, name="Task")
        datakey = ["fileName","userId","jobID","jobStatus","uploadUrl","local"]
        mysqlSaveDict = {key: message_json.get(key) for key in datakey}


        async def save_or_update_task(mysqlSaveDict):
            await Tortoise.init(
                db_url='mysql://root:e8c87vb2@118.195.223.193:3306/imputationcomputed',
                modules={'models': ['models.task']}
            )

            job_id = mysqlSaveDict['jobID']
            # 尝试获取具有相同jobID的任务
            existing_task = await Task.get_or_none(jobID=job_id)

            if existing_task:
                # 如果存在相同jobID的任务，则更新现有记录
                await Task.filter(jobID=job_id).update(**mysqlSaveDict)
                print("update")
            else:
                # 如果不存在相同jobID的任务，则创建新记录
                await Task.create(**mysqlSaveDict)
                print("creat")
        run_async(save_or_update_task(mysqlSaveDict))
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









