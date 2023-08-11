# 使用官方 Python 3.10 镜像作为基础
FROM python:3.10

# 设置工作目录
WORKDIR /app
# 安装 rsync 和 tabix
RUN apt-get update && apt-get install -y rsync tabix openssh-server


# 将当前目录下的 requirements.txt 文件复制到容器中
COPY rsync_submit_Part/ .
COPY rsync_submit_Part/requirements.txt .
# 安装所需的依赖包
RUN pip install --no-cache-dir --user -r ./requirements.txt

# 复制应用程序代码到容器中
COPY . .

# 设置环境变量，如果需要的话
# ENV VARIABLE_NAME value

# 运行应用程序并将日志输出到文件
CMD python rsync_submit_Part/apscheduler_jobs.py >> /app/logapscheduler 2>&1 & python rsync_submit_Part/custumerRsyncSingleQueue.py >> /app/logcustumer 2>&1
