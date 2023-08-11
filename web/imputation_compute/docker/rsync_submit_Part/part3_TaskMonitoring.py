import json
import pika
import time
import redis
import config as c
import requests
import asyncio
from jobstart import submit_workflow_to_server

#### CONFIG ######INFO
redis_host = c.redishost
redis_port = c.redisport
redis_password = c.redispassword
redis_Queue_rsync = c.redisQueue_rsync
radis_Queue_submit = c.redisQueue_submit
QUEUE_NAME="queueUUID"
######################

def uuidWrite(uuid,status):
    jobsStatusDict = {"UUID":uuid,"status":status}
    uuid_status_file = c.uuidStatusFile

    with open(uuid_status_file,"wa") as f:
        json.dump(jobsStatusDict, f)
    print(f"uuid alrady write to file {uuid_status_file}...")


def statusCheck():
    import redis

    # 创建Redis客户端
    r = redis.Redis(host=redis_host, port=6379, db=1,password=redis_password)

    # 检查任务状态
    def check_task_status():
                # 从Redis中获取任务状态
                done=None
                tasks = []
                for uuid in r.keys():
                    message = json.loads(r.get(uuid).decode())
                    status = message.get("jobStatus")
                    if status not in ['Succeeded', 'Failed',"Abort"]:
                        # 如果状态不存在，则表示任务需要进行状态检查
                        # 这里可以编写您自己的逻辑，例如通过API查询任务状态
                        # 假设查询逻辑返回的任务状态为new_status
                        # 如果状态存在，则检查是否发生了改变

                        # 假设查询逻辑返回的任务状态为new_status
                        #new_status = 'in_progress'  # 假设新的任务状态为'in_progress'


                                # 如果新状态不是最终状态，继续处理任务
                        # task = asyncio.create_task(process_task(uuid))
                        # tasks.append(task)
                        return_status = checkUUID(uuid.decode())
                        #print(return_status)
                        return_status= json.loads(return_status)
                        message["jobStatus"] = return_status.get("status")
                        message = json.dumps(message)
                        r.set(return_status.get("id"),message.encode())
                # if tasks:
                #     done, pending = await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)
                #     for task in done:
                #         return_status = task.result()
                #         print(return_status)
                #         r.set(return_status.get("uuid"),return_status.get("status"))

    check_task_status()





def checkUUID(uuid):
    #print( c.url + f"/{uuid}/status")
    requests_out = requests.get(
        c.url + f"/{uuid}/status"
    )
    return (requests_out.text)

def main():
    from redis_queue import Queue
    m = Queue(QUEUE_NAME, host=redis_host, port=redis_port, password=redis_password)
    print(f"{QUEUE_NAME} connect")


    while 1:
        ## check queue is empty
        if m.empty():
            time.sleep(1)
        else:
            m.get_nowait()
            print(str(m))

            connection = pika.BlockingConnection(
                pika.ConnectionParameters('192.168.77.45', 5672, '/', pika.PlainCredentials('guest', 'guest')))
            channel = connection.channel()
            print(f"rabbitMQ connect")
            # 创建一个指定名称的交换机，并指定类型为fanout，用于将接收到的消息广播到所有queue中
            channel.exchange_declare(exchange='exange_QUEUE_UUID', exchange_type='fanout')

            message = str(m).encode()
            # 将消息发送给指定的交换机，在fanout类型中，routing_key=''表示不用发送到指定queue中，
            # 而是将发送到绑定到此交换机的所有queue
            channel.basic_publish(exchange='exange_QUEUE_UUID', routing_key='', body=message)
            print(" [x] Sent %r" % message)
            connection.close()
if __name__ == '__main__':
    main()