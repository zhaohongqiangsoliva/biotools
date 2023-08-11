#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: soliva
@Site: 
@file: apscheduler_jobs.py
@time: 2023/7/9
@desc:
'''


from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

#### base founction
import logging
import datetime
import json
#### module of selfs
from redis_queue import Queue
from jobstart import submit_workflow_to_server
import config as c
#JOBS module
from part1_rsync import *
from part2_submit_cromwell  import dealWithcromwellJOBS,update_config
from part3_TaskMonitoring import *
from part4_minioCli import *


def nextQueue(message,queue):


    NextQueue_message = json.dumps(message, indent=4)
    s = Queue(queue, host=redis_host, port=redis_port, password=redis_password)
    s.put_nowait(NextQueue_message)


def message_update(message,addDict):
    update_config(message,addDict)

def part1_Rsync():
    m = Queue("queueRsync", host=redis_host, port=redis_port, password=redis_password)

    if not  m.empty():
        message = m.get_nowait()#.decode("utf-8")
        logging.warning("part1_Rsync  ---  " + message)

        ## write str to dict
        message = json.loads(message)
        fileName = message.get("fileName")
        filePath = message.get("filePath")
        suffixName = message.get("suffixName")
        userId = message.get("userId")
        fileId = message.get("fileId")
        source = filePath + fileName + suffixName
        destination = imputationWorkPath + userId + "/"
        message["source"] = source
        message["destination"] = destination
        # send path to rsync
        jobCheck = asyncio.run(
            runQuery([{"source": f"{target}:{source}", "destination": f"{destination}"}]))  # soliva@192.168.77.45:~/
        logging.warning(jobCheck)
        for k, v in jobCheck.items():
            if v == 0:
                logging.warning(f"id:{userId} fileName:{fileName} Rsync success")
                nextQueue(message,"queueSubmit")

            else:

                logging.warning(f"fail,the return code is {v}  \nmeans:{c.rsync_return_codes[v]}")

# 任务执行函数
def part2_CromwellSubmit():
    redis_host = c.redishost
    redis_port = c.redisport
    redis_password = c.redispassword


    m = Queue("queueSubmit", host=redis_host, port=redis_port, password=redis_password)
    #print("queueSubmit connect")
    if not m.empty():
        destination = m.get_nowait()
        logging.warning("part2_CromwellSubmit --- " + destination)


        cromwell_json, cromwell_options = dealWithcromwellJOBS(destination)
        message = json.loads(destination)
        cromwell_message = submit_workflow_to_server(
            c.url,
            c.cromwell_wdl,
            cromwell_json,
            cromwell_options,
            c.cromwell_zip)
        # submit_workflow_to_server
        cromwell_message = json.loads(cromwell_message)
        message["jobID"] = cromwell_message["id"]
        message["jobStatus"] = cromwell_message["status"]

        nextQueue(message, "queueUUID")
    #print('job %s is runed at %s' % (job_id, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

def part3_TaskMonitoring():



    #print(f"{QUEUE_NAME} connect")
    def put_rabbit(message,exchange):
        import uuid
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(c.rabbitmqhost, 5672, '/', pika.PlainCredentials(c.rabbitmqusername, c.rabbitmqpassword)))
        channel = connection.channel()
        #print(f"rabbitMQ connect")
        # 创建一个指定名称的交换机，并指定类型为fanout，用于将接收到的消息广播到所有queue中
        channel.exchange_declare(exchange=exchange, exchange_type='fanout')
        message_id = str(uuid.uuid4())
        properties = pika.BasicProperties(
            message_id=message_id,
            # 其他属性设置，如持久化等
        )
        #message = str(m).encode()

        # 将消息发送给指定的交换机，在fanout类型中，routing_key=''表示不用发送到指定queue中，
        # 而是将发送到绑定到此交换机的所有queue
        channel.basic_publish(exchange=exchange, routing_key='', body=message,properties=properties)
        logging.warning(" [success] Sent %r" % message)
        connection.close()


    # 创建Redis客户端
    r = redis.Redis(host=c.redishost, port=6379, db=1,password=c.redispassword)

    QUEUE_NAME = "queueUUID"
    m = Queue(QUEUE_NAME, host=redis_host, port=redis_port, password=redis_password)

    ## check queue is empty
    if not m.empty():
        message = m.get_nowait()
        logging.warning("part3_TaskMonitoring --- " + message)

        message_json = json.loads(message)
        print(message_json)
        '''
        {
    "fileName": "3341231",
    "filePath": "/home/shupeng/imputation/uploadfiles/115110151301/535684274d9d985d7e9200b459ed0137/3341231/",
    "suffixName": ".vcf.gz",
    "userId": "1",
    "fileId": "1383396952899584",
    "source": "/home/shupeng/imputation/uploadfiles/115110151301/535684274d9d985d7e9200b459ed0137/3341231/3341231.vcf.gz",
    "destination": "/disk/project/imputation/imputation_web/userDATA/1/"
}
        '''
        checkUUID_Return =  checkUUID(message_json.get("jobID"))
        jobStatus = json.loads(checkUUID_Return)
        uuid = jobStatus.get("id")
        status = jobStatus.get("status")
        message_json["jobStatus"] = status
        message_json["uploadUrl"] = ""
        redis_message_json= json.dumps(message_json)
        print(uuid,redis_message_json.encode())
        r.set(uuid,redis_message_json.encode())

        put_rabbit(redis_message_json,"exange_QUEUE_UUID")
    else:
        ### 检查状态后放入rabbit mq

        statusCheck()
        for uuid in r.keys():

            uuid = uuid.decode()
            message = r.get(uuid)
            message_json = json.loads(message)
            #statusCheck(message_json)
            message_json["uploadUrl"] = ""
            status = message_json.get("jobStatus")

            logging.warning(f"part3_TaskMonitoring --- Check Running Jobs:{uuid} {status}" )


            if status in [ 'Failed',"Aborted"]:
                #logging.warning("part3_TaskMonitoring --- Check Running Jobs" + uuid)
                message_json["jobID"] = uuid
                message_json["jobStatus"] = status
                toRabbitjson = json.dumps(message_json)
                put_rabbit(toRabbitjson,'exange_QUEUE_UUID')
                r.delete(uuid)
            elif  status in  ['Succeeded']:
                message_json["jobID"] = uuid
                message_json["jobStatus"] = status
                ### if succeeded upload to minio server

                rsyncPushSource = c.imputationWorkPath +"/"  + message_json.get("userId") +"/" + "cromwell/output"


                user = message_json.get("userId")
                project = message_json.get("fileName")

                object_path = f"output/{user}/{project}"
                bucket_name = c.minioBucket_name #"imputation"
                # object_name = "test"  # Name of the object when stored in MinIO
                minio_endpoint = c.minio_endpoint #"118.195.223.193:9000"  # For example, "play.minio.io:9000"
                access_key = c.minioAccessKey 
                secret_key = c.minioSecrtKey
                folder_path = rsyncPushSource
                
                uploaded_file_url = upload_to_minio(access_key, secret_key, bucket_name, folder_path, object_path, minio_endpoint)
                
                
                
                message_json["uploadUrl"] = uploaded_file_url
                #f"{minio_endpoint}/{bucket_name}/{object_path}"
                toRabbitjson = json.dumps(message_json)
                put_rabbit(toRabbitjson,'exange_QUEUE_UUID')
                r.delete(uuid)
                print("Uploaded File JSON:", toRabbitjson)

                
    r.close()




# 事件监听
def job_exception_listener(Event):
    job = scheduler.get_job(Event.job_id)
    if  Event.exception:
    #     logging.warning()("jobname=%s|jobtrigger=%s|jobtime=%s|retval=%s", job.name, job.trigger,
    #                 Event.scheduled_run_time, Event.retval)
    # else:
        logging.error("jobname=%s|jobtrigger=%s|errcode=%s|exception=[%s]|traceback=[%s]|scheduled_time=%s", job.name,
                     job.trigger, Event.code,
                     Event.exception, Event.traceback, Event.scheduled_run_time)





# 日志
logging.basicConfig(format='%(asctime)s %(message)s',  datefmt='%m/%d/%Y %I:%M:%S %p' ,level=logging.WARNING)
logging.getLogger('apscheduler')#.setLevel(logging.DEBUG)

# 定义一个后台任务非阻塞调度器
scheduler = BackgroundScheduler()
# 添加一个任务到内存中
# 触发器：trigger='interval' seconds=10 每10s触发执行一次
# 执行器：executor='default' 线程执行
# 任务存储器：jobstore='default' 默认内存存储
# 最大并发数：max_instances
scheduler.add_job(part1_Rsync, trigger='interval', seconds=10)

scheduler.add_job(part2_CromwellSubmit, trigger='interval', seconds=10)

scheduler.add_job(part3_TaskMonitoring, trigger='interval', seconds=30)
# 设置任务监听
scheduler.add_listener(job_exception_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

# 启动调度器
scheduler.start()
#scheduler.print_jobs()
try:
    while True:
        pass
except KeyboardInterrupt:
    pass

# 关闭调度器
scheduler.shutdown()

#:TODO
#1. JOBS：Rabbitmq message receive to rsync control  ----queue 1
#2. JOBS: rsync control to submit cromwell ----queue 1
#3. JOBS: submit cromwell to jobs monitor -----queue 1
#4. JOBS: jobs monitor  running or finish  then  return to  web server 1
#5. JOBS: jobs re-download use rsync 1
#6. JOBS: run meta-imputation
#7. JOBS: rsync push to web server