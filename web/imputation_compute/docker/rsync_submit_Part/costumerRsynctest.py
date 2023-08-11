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

def send2Shanghai(message:str):
    import pika
    import uuid
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('118.195.223.193', 5672, '/', pika.PlainCredentials('prs_hub', 'zcygkc36')))
    channel = connection.channel()

    # 创建消息属性，设置唯一标识符
    message_id = str(uuid.uuid4())
    properties = pika.BasicProperties(
        message_id=message_id,
        # 其他属性设置，如持久化等
    )

    # 创建一个指定名称的交换机，并指定类型为fanout，用于将接收到的消息广播到所有queue中
    channel.exchange_declare(exchange='imputation.upload.file.queue.shanghai', exchange_type='fanout')
    #message.encode()
    # 将消息发送给指定的交换机，在fanout类型中，routing_key=''表示不用发送到指定queue中，
    # 而是将发送到绑定到此交换机的所有queue
    channel.basic_publish(exchange='imputation.upload.file.queue.shanghai', routing_key='', body=message,
                          properties=properties)
    print(" [x] Sent %r" % message)
    connection.close()


def callback(ch, method, properties, body):
    # 将接收到的消息解析为任务信息
    message  = body
    print(message)
    send2Shanghai(message)
    ### using redis queue Persistence queue
    q = Queue("queueRsync", host=redis_host, port=redis_port, password=redis_password)
    message_json = json.loads(message)
    message_json["local"] = c.local
    message = json.dumps(message_json)
    send_queue = q.put_nowait(message)

    # if send_queue == True:
    #     ch.basic_ack(delivery_tag=method.delivery_tag)

    # 执行任务
    print("message" ,"alrady join to qeueue")



connection = pika.BlockingConnection(
    pika.ConnectionParameters(rabbitmq_host,5672, '/', pika.PlainCredentials(rabbitmq_username,rabbitmq_password)))
    #pika.ConnectionParameters('192.168.77.45',5672, '/', pika.PlainCredentials('guest','guest')))
channel = connection.channel()

# result = channel.queue_declare(queue='', exclusive=True)
# queue_name_2 = result.method.queue
# channel.queue_bind(exchange='my_exchange', queue=queue_name_2)
# # 声明队列
# # channel.queue_declare(queue='task_queue')
# channel.basic_consume(queue=queue_name_2, on_message_callback=callback, auto_ack=False)
# 消费者订阅队列，并指定回调函数处理消息


#channel.queue_declare(queue='imputation.upload.file.queue.shanghai',durable=True)
channel.basic_consume(queue='imputation.upload.file.queue.beijing', on_message_callback=callback, auto_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
# 启动消费者循环，持续等待任务到达并处理
channel.start_consuming()