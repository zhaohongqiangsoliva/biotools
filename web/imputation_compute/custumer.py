#!/usr/bin/env python
import pika
import  time
import json
import asyncio
#from rsync_submit_Part import runQuery

connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.77.45',5672, '/', pika.PlainCredentials('guest','guest')))
channel = connection.channel()

# redis_host = c.redishost
# redis_port = c.redisport
# redis_password = c.redispassword
# rabbitmq_host = "192.168.77.45"#c.rabbitmqhost
# rabbitmq_port = c.rabbitmqport
# rabbitmq_username = "guest" #c.rabbitmqusername
# rabbitmq_password = "guest"#c.rabbitmqpassword

def callback(ch, method, properties, body):
    # 将接收到的消息解析为任务信息
    message  = body
    print(message)

    ### using redis queue Persistence queue
    # q = Queue("queueRsync", host=redis_host, port=redis_port, password=redis_password)
    # send_queue = q.put_nowait(message)
    # if send_queue == True:
    #     ch.basic_ack(delivery_tag=method.delivery_tag)

    # 执行任务
    print("message" ,"alrady join to qeueue")
#
#
#
# connection = pika.BlockingConnection(
#     pika.ConnectionParameters(rabbitmq_host,5672, '/', pika.PlainCredentials(rabbitmq_username,rabbitmq_password)))
#     #pika.ConnectionParameters('192.168.77.45',5672, '/', pika.PlainCredentials('guest','guest')))
# channel = connection.channel()

result = channel.queue_declare(queue='', exclusive=True)
queue_name_2 = result.method.queue
channel.queue_bind(exchange='exange_QUEUE_UUID', queue=queue_name_2)
# 声明队列
# channel.queue_declare(queue='task_queue')
channel.basic_consume(queue=queue_name_2, on_message_callback=callback, auto_ack=False)
#消费者订阅队列，并指定回调函数处理消息


#channel.queue_declare(queue='imputation.upload.file.queue.shanghai',durable=True)
#channel.basic_consume(queue='imputation.upload.file.queue.beijing', on_message_callback=callback, auto_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
# 启动消费者循环，持续等待任务到达并处理
channel.start_consuming()


