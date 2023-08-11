#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: soliva
@Site: 
@file: custumerRsyncMutilQueue.py
@time: 2023/7/5
@desc:
'''
import asyncio
import subprocess
from queue import Queue
import pika

async def run_rsync(source, destination):
    command = ['rsync', '-av', source, destination]
    process = await asyncio.create_subprocess_exec(*command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = await process.communicate()
    return process.returncode, stdout.decode(), stderr.decode()

async def process_task_queue(task_queue):
    while True:
        # 从任务队列中获取任务
        source, destination = task_queue.get()

        # 如果获取到的任务是特殊标记，表示任务队列已完成，退出循环
        if source is None and destination is None:
            break

        # 执行任务
        returncode, stdout, stderr = await run_rsync(source, destination)

        # 处理返回值
        print(f"Task: Return code={returncode}, Stdout={stdout}, Stderr={stderr}")

        # 标记任务完成
        task_queue.task_done()

async def consume_tasks():
    # 创建任务队列
    task_queue = Queue()

    # 创建任务处理协程
    task_processor = asyncio.create_task(process_task_queue(task_queue))

    # 连接到 RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # 声明队列
    channel.queue_declare(queue='task_queue')

    def callback(ch, method, properties, body):
        # 将接收到的消息解析为任务信息
        source, destination = body.decode().split(',')

        # 将任务添加到任务队列中
        task_queue.put((source, destination))

    # 消费者订阅队列，并指定回调函数处理消息
    channel.basic_consume(queue='task_queue', on_message_callback=callback, auto_ack=True)

    # 启动消费者循环，持续等待任务到达并处理
    channel.start_consuming()

    # 添加特殊标记到任务队列，以通知任务处理协程退出循环
    task_queue.put((None, None))

    # 等待任务处理协程结束
    await task_processor

    # 关闭连接
    connection.close()

# 运行消费者任务
asyncio.run(consume_tasks())
