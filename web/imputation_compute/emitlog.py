import pika
import uuid
connection = pika.BlockingConnection(
    pika.ConnectionParameters('118.195.223.193',5672, '/', pika.PlainCredentials('prs_hub','zcygkc36')))
channel = connection.channel()

# 创建消息属性，设置唯一标识符
message_id = str(uuid.uuid4())
properties = pika.BasicProperties(
    message_id=message_id,
    # 其他属性设置，如持久化等
)

# 创建一个指定名称的交换机，并指定类型为fanout，用于将接收到的消息广播到所有queue中
channel.exchange_declare(exchange='imputation.upload.file.queue.shanghai', exchange_type='fanout')

message = b"""{"fileName": "3341231", "filePath": "/home/shupeng/imputation/uploadfiles/115110151301/535684274d9d985d7e9200b459ed0137/3341231/","local":"beijing", "suffixName": ".vcf.gz", "userId": "1", "fileId": "1383396952899584", "source": "/home/shupeng/imputation/uploadfiles/115110151301/535684274d9d985d7e9200b459ed0137/3341231/3341231.vcf.gz", "destination": "/disk/project/imputation/imputation_web/userDATA/1/", "jobID": "e28a2efc-7496-449d-b2f7-d8316e4e2284", "jobStatus": "running", "uploadUrl": ["http://118.195.223.193:9000/imputation/output/1/3341231/3341231.dose.vcf.gz.tbi", "http://118.195.223.193:9000/imputation/output/1/3341231/3341231.dose.vcf.gz", "http://118.195.223.193:9000/imputation/output/1/3341231/3341231.empiricalDose.vcf.gz", "http://118.195.223.193:9000/imputation/output/1/3341231/3341231_aggregated_imputation_metrics.tsv", "http://118.195.223.193:9000/imputation/output/1/3341231/n_failed_chunks.txt", "http://118.195.223.193:9000/imputation/output/1/3341231/3341231_chunk_info.tsv", "http://118.195.223.193:9000/imputation/output/1/3341231/3341231.vcf.gz.tbi", "http://118.195.223.193:9000/imputation/output/1/3341231/3341231_failed_chunks.tsv", "http://118.195.223.193:9000/imputation/output/1/3341231/3341231.vcf.gz", "http://118.195.223.193:9000/imputation/output/1/3341231/3341231.empiricalDose.vcf.gz.tbi"]}"""
# 将消息发送给指定的交换机，在fanout类型中，routing_key=''表示不用发送到指定queue中，
# 而是将发送到绑定到此交换机的所有queue
channel.basic_publish(exchange='imputation.upload.file.queue.shanghai', routing_key='', body=message,properties=properties)
print(" [x] Sent %r" % message)
connection.close()
