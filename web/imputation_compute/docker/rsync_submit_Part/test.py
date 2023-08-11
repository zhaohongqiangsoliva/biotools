from redis_queue import Queue
import config as c
redis_host = c.redishost
redis_port = c.redisport
redis_password = c.redispassword
redis_Queue_rsync = c.redisQueue_rsync
radis_Queue_submit = c.redisQueue_submit
NextQueue_message = "flake_UUIDS"
# submit_workflow_to_server
test = """{"fileName":"3341231","filePath":"/home/shupeng/imputation/uploadfiles/115110151301/535684274d9d985d7e9200b459ed0137/3341231/","suffixName":".vcf.gz","userId":"1","fileId":"1383396952899584","source": "/home/shupeng/imputation/uploadfiles/115110151301/535684274d9d985d7e9200b459ed0137/3312132222/3312132222.vcf.gz", "destination": "soliva@192.168.77.45:/disk/project/imputation/imputation_web/userDATA/","local":"beijing"}"""
test2 = """{    "fileName": "3341231",
    "filePath": "/home/shupeng/imputation/uploadfiles/115110151301/535684274d9d985d7e9200b459ed0137/3341231/",
    "suffixName": ".vcf.gz",
    "userId": "1",
    "fileId": "1383396952899584",
    "source": "/home/shupeng/imputation/uploadfiles/115110151301/535684274d9d985d7e9200b459ed0137/3341231/3341231.vcf.gz",
    "destination": "/disk/project/imputation/imputation_web/userDATA/1/",
    "jobStatus":"Failed",
    "jobID":"d9118d5c-afe6-46c5-955e-ff32c29fd415",
    "uploadUrl":
    }"""
# s = Queue("queueRsync", host=redis_host,
#           port=redis_port, password=redis_password)
# s.put_nowait(test)

test3 = '''
{"fileName": "3341231", "filePath": "/home/shupeng/imputation/uploadfiles/115110151301/535684274d9d985d7e9200b459ed0137/3341231/","local":"beijing", "suffixName": ".vcf.gz", "userId": "1", "fileId": "1383396952899584", "source": "/home/shupeng/imputation/uploadfiles/115110151301/535684274d9d985d7e9200b459ed0137/3341231/3341231.vcf.gz", "destination": "/disk/project/imputation/imputation_web/userDATA/1/", "jobID": "e28a2efc-7496-449d-b2f7-d8316e4e2284", "jobStatus": "running", "uploadUrl": ["http://118.195.223.193:9000/imputation/output/1/3341231/3341231.dose.vcf.gz.tbi", "http://118.195.223.193:9000/imputation/output/1/3341231/3341231.dose.vcf.gz", "http://118.195.223.193:9000/imputation/output/1/3341231/3341231.empiricalDose.vcf.gz", "http://118.195.223.193:9000/imputation/output/1/3341231/3341231_aggregated_imputation_metrics.tsv", "http://118.195.223.193:9000/imputation/output/1/3341231/n_failed_chunks.txt", "http://118.195.223.193:9000/imputation/output/1/3341231/3341231_chunk_info.tsv", "http://118.195.223.193:9000/imputation/output/1/3341231/3341231.vcf.gz.tbi", "http://118.195.223.193:9000/imputation/output/1/3341231/3341231_failed_chunks.tsv", "http://118.195.223.193:9000/imputation/output/1/3341231/3341231.vcf.gz", "http://118.195.223.193:9000/imputation/output/1/3341231/3341231.empiricalDose.vcf.gz.tbi"]}

'''
print(test3)

s = Queue("queueUUID", host=redis_host,
          port=redis_port, password=redis_password)
s.put_nowait(test3)

'''
{"fileName": "3341231", "filePath": "/home/shupeng/imputation/uploadfiles/115110151301/535684274d9d985d7e9200b459ed0137/3341231/", "suffixName": ".vcf.gz", "userId": "1", "fileId": "1383396952899584", "source": "/home/shupeng/imputation/uploadfiles/115110151301/535684274d9d985d7e9200b459ed0137/3341231/3341231.vcf.gz", "destination": "/disk/project/imputation/imputation_web/userDATA/1/", "jobID": "c02ace2a-685e-4dfe-96a7-f2ca9067d013", "jobStatus": "Succeeded", "uploadUrl": ["http://118.195.223.193:9000/imputation/output/1/3341231/3341231.dose.vcf.gz.tbi", "http://118.195.223.193:9000/imputation/output/1/3341231/3341231.dose.vcf.gz", "http://118.195.223.193:9000/imputation/output/1/3341231/3341231.empiricalDose.vcf.gz", "http://118.195.223.193:9000/imputation/output/1/3341231/3341231_aggregated_imputation_metrics.tsv", "http://118.195.223.193:9000/imputation/output/1/3341231/n_failed_chunks.txt", "http://118.195.223.193:9000/imputation/output/1/3341231/3341231_chunk_info.tsv", "http://118.195.223.193:9000/imputation/output/1/3341231/3341231.vcf.gz.tbi", "http://118.195.223.193:9000/imputation/output/1/3341231/3341231_failed_chunks.tsv", "http://118.195.223.193:9000/imputation/output/1/3341231/3341231.vcf.gz", "http://118.195.223.193:9000/imputation/output/1/3341231/3341231.empiricalDose.vcf.gz.tbi"]}

'''