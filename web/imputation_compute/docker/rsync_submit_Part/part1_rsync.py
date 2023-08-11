import asyncio
import subprocess
import config
import time
import logging as log
import config as c
import json
redis_host = c.redishost
redis_port = c.redisport
redis_password = c.redispassword
redis_Queue_rsync = c.redisQueue_rsync
imputationWorkPath = c.imputationWorkPath
target = c.target_server
async def run_rsync(source, destination):
    # 构造rsync命令
    command = ['rsync',"-avzrtP" ,  "--info=progress2", "-e", "ssh -p 22", source, destination]#

    # 启动子进程执行rsync命令
    process = await asyncio.create_subprocess_exec(*command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=False)

    # 等待命令执行完成并获取返回值
    stdout, stderr = await process.communicate()

    # 返回返回值和命令输出
    return process.returncode, stdout, stderr


async def runQuery(jobList):
    # 定义要执的rsync任务
    tasks = []
    for lists  in jobList:
        print(lists)
        source=lists["source"]
        destination=lists["destination"]
        tasks.append(run_rsync(source, destination))
    # 并行执行任务
    results = await asyncio.gather(*tasks)

    # 处理返回值
    jobCheck = {}
    for i, result in enumerate(results):
        returncode, stdout, stderr = result
        log.info(f"Task {i + 1}: Return code={returncode}")
        jobCheck[i]=returncode
    return jobCheck


if __name__ == '__main__':

    from redis_queue import Queue
    m = Queue("queueRsync", host=redis_host, port=redis_port, password=redis_password)
    print("queueRsync connect")
    while 1:
        ## check queue is empty
        if m.empty():
            time.sleep(1)
        else:
            message=m.get_nowait().decode()
            print(message)
            ## write str to dict
            message = json.loads(message)
            fileName= message.get("fileName")
            filePath = message.get("filePath")
            suffixName = message.get("suffixName")
            userId = message.get("userId")
            fileId = message.get("fileId")
            source = filePath + fileName + suffixName
            destination = imputationWorkPath + userId +"/"
            message["source"] = source
            message["destination"] = destination
            NextQueue_message = json.dumps(message,  indent=4)
            #send path to rsync
            jobCheck = asyncio.run(
                runQuery([{"source": f"{source}", "destination": f"{target}:{destination}"}]))  # soliva@192.168.77.45:~/
            print(jobCheck)
            for k, v in jobCheck.items():
                if v == 0:
                    print("success")
                    s = Queue("queueSubmit", host=redis_host, port=redis_port, password=redis_password)
                    s.put_nowait(NextQueue_message)
                else:

                    print(f"fail,the return code is {v}  \nmeans:{c.rsync_return_codes[v]}")











