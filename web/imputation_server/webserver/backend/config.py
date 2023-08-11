# config.py
url="http://192.168.77.45:8088/api/workflows/v1"
imputationWorkPath="/disk/project/imputation/imputation_web/userDATA/"
target_server="soliva@192.168.77.45"
local = "beijing"
#    redis args
redishost="192.168.77.45"
redisport=6379
redispassword="123942"
redisQueue_rsync="queueRsync"
redisQueue_submit="queueRsync"



#   rabbitmq args
rabbitmqhost='118.195.223.193'
rabbitmqport=5672
rabbitmqusername='prs_hub'
rabbitmqpassword='zcygkc36'



cromwell_wdl="/disk/project/imputation/warp19/Imputation_v1.1.10.wdl"
cromwell_json="/disk/project/imputation/warp19/input_2.json"
cromwell_option="/disk/project/imputation/warp19/options.json"
cromwell_zip="/disk/project/imputation/warp19/Imputation_v1.1.10.zip"

## minio accesskey with serctkey
minioAccessKey = "JnHKZFBpgwRDVL02AM0h"
minioSecrtKey = "gLWKCG6OvclTHT9vJcc7EZSOCW4V7s0evjqLhG2r"
minio_endpoint = "118.195.223.193:9000"
minioBucket_name = "imputation"


#Rsync errorList
rsync_return_codes = {
    0: "Success",
    1: "Syntax or usage error",
    2: "Protocol incompatibility",
    3: "Errors selecting input/output files, dirs",
    4: "Requested action not supported",
    5: "Error starting client-server protocol",
    6: "Daemon unable to append to log-file",
    10: "Error in socket I/O",
    11: "Error in file I/O",
    12: "Error in rsync protocol data stream",
    13: "Errors with program diagnostics",
    14: "Error in IPC code",
    20: "Received SIGUSR1 or SIGINT",
    21: "Some error returned by waitpid()",
    22: "Error allocating core memory buffers",
    23: "Partial transfer due to error",
    24: "Partial transfer due to vanished source files",
    25: "The --max-delete limit stopped deletions",
    30: "Timeout in data send/receive",
    35: "Timeout waiting for daemon connection"
}