import schedule
import time,os
from datetime import datetime

# current datetime




# 定义你要周期运行的函数
def job():
    now = datetime.now()
    current_date = now.date()
    os.system("""find /work/share/ac7m4df1o5/bin/cromwell/cromwell-executions -name "slurm-*out" -exec grep -n "STARTING" {} \; >/work/share/ac7m4df1o5/bin/cromwell/deludocker.list && cat /work/share/ac7m4df1o5/bin/cromwell/deludocker.list|sh /work/share/ac7m4df1o5/bin/cromwell/2.except.sh|awk '{print "rsync --delete-before -d /work/share/ac7m4df1o5/bin/cromwell/empty/ /work/share/ac7m4df1o5/bin/cromwell/.udocker/containers/"$1"/"}'  >/work/share/ac7m4df1o5/bin/cromwell/rm.log && parallel -j 10 < /work/share/ac7m4df1o5/bin/cromwell/rm.log """)
    time.time()
    print('Date:', current_date)
schedule.every().hour.do(job)                    # 每隔 1 小时运行一次 job 函数


while True:
    schedule.run_pending()   # 运行所有可以运行的任务
    time.sleep(1)