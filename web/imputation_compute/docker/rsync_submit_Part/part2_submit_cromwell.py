#!/usr/local/env bash
import time
import json
import config as c
import os
from jobstart import submit_workflow_to_server


redis_host = c.redishost
redis_port = c.redisport
redis_password = c.redispassword
redis_Queue_rsync = c.redisQueue_rsync
radis_Queue_submit = c.redisQueue_submit

# c.cromwell_wdl="/disk/project/imputation/warp19/Imputation_v1.1.10.wdl"
# c.cromwell_json="/disk/project/imputation/warp19/input_2.json"
# c.cromwell_option="/disk/project/imputation/warp19/options.json"
# c.cromwell_zip="/disk/project/imputation/warp19/Imputation_v1.1.10.zip"








def update_config(config, config_updates):
    '''
    递归 config json 文件更新字典，

    '''
    for key, value in config_updates.items():
        if key in config:
            if isinstance(value, dict) and isinstance(config[key], dict):
                update_config(config[key], value)  # 递归处理嵌套的字典
            else:
                config[key] = value


def update_config_files(config, config_updates):
    "更新json文件"
    # 遍历配置文件目录

    with open(config, "r") as f:
        config_data = json.load(f)

    # 更新配置项
    update_config(config_data, config_updates)

    return (json.dumps(config_data,  indent=4))


def dealWithcromwellJOBS(message):
    message = json.loads(message)
    remote_file = c.imputationWorkPath + message.get("userId") +"/" + message.get("fileName") +  message.get("suffixName")

    if os.path.exists(remote_file +  ".tbi") :
        pass
    else:
        os.system(f"""tabix {remote_file}""")

    if os.path.exists(c.imputationWorkPath +"/"  + message.get("userId") +"/" + "cromwell/output"):
        pass
    else:
        os.system(f"""mkdir -pv {c.imputationWorkPath +"/"  + message.get("userId") +"/" + "cromwell/{output,log,call_log}"}""")

    input_json_modify = {
        "Imputation.multi_sample_vcf": remote_file,
        "Imputation.multi_sample_vcf_index": remote_file +  ".tbi",
        "Imputation.contigs":["22"],
        "Imputation.output_callset_name":message.get("fileName")
    }
    option_json_modify = {
        "final_workflow_outputs_dir": c.imputationWorkPath +"/"  + message.get("userId") +"/" + "cromwell/output",
        "final_workflow_log_dir": c.imputationWorkPath +"/" + message.get("userId") +"/" + "cromwell/log",
        "final_call_logs_dir": c.imputationWorkPath +"/" + message.get("userId") +"/" + "cromwell/call_log"
    }
    cromwell_json = update_config_files(c.cromwell_json,input_json_modify,)
    cromwell_options= update_config_files(c.cromwell_option,option_json_modify,)
    return cromwell_json , cromwell_options

#test = """{"fileName":"3341231","filePath":"/home/shupeng/imputation/uploadfiles/115110151301/535684274d9d985d7e9200b459ed0137/3341231/","suffixName":".vcf.gz","userId":"1","fileId":"1383396952899584","source": "/home/shupeng/imputation/uploadfiles/115110151301/535684274d9d985d7e9200b459ed0137/3312132222/3312132222.vcf.gz", "destination": "soliva@192.168.77.45:/disk/project/imputation/imputation_web/userDATA1/"}"""
#cromwell_json , cromwell_options = dealWithcromwellJOBS(test)
#print(cromwell_json , cromwell_options )
if __name__ == '__main__':
    from redis_queue import Queue

    m = Queue("queueSubmit", host=redis_host, port=redis_port, password=redis_password)
    print("queueSubmit connect")
    while 1:
        ## check queue is empty
        if m.empty():
            time.sleep(1)
        else:
            a=m.get_nowait()
            print(a)
            destination = a
            cromwell_json, cromwell_options = dealWithcromwellJOBS(destination)
            open(c.cromwell_zip,)
            NextQueue_message = submit_workflow_to_server(
                c.url,
                c.cromwell_wdl,
                    cromwell_json,
                    cromwell_options,
                    c.cromwell_zip)
            #submit_workflow_to_server
            s = Queue("queueUUID", host=redis_host, port=redis_port, password=redis_password)
            s.put_nowait(NextQueue_message)











