
import pika

# 建立 RabbitMQ 连接
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.77.45',5672, '/', pika.PlainCredentials('guest','guest')))
channel = connection.channel()

# 声明一个 Fanout 类型的交换机
channel.exchange_declare(exchange='my_exchange', exchange_type='fanout')

# 声明两个队列，并将它们绑定到交换机上
result = channel.queue_declare(queue='', exclusive=True)
queue_name_1 = result.method.queue
channel.queue_bind(exchange='my_exchange', queue=queue_name_1)

result = channel.queue_declare(queue='', exclusive=True)
queue_name_2 = result.method.queue
channel.queue_bind(exchange='my_exchange', queue=queue_name_2)

# 定义回调函数，处理收到的消息
def callback(ch, method, properties, body):
    print("Received message:", body)

# 启动两个消费者分别监听两个队列
channel.basic_consume(queue=queue_name_1, on_message_callback=callback, auto_ack=True)
channel.basic_consume(queue=queue_name_2, on_message_callback=callback, auto_ack=True)

# 开始接收消息
channel.start_consuming()