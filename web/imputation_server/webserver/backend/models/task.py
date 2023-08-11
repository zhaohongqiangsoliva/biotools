from tortoise import models
from tortoise import fields


class Task(models.Model):
    # id = fields.CharField(max_length=50, null=False, description="id")
    fileName = fields.CharField(max_length=50, null=False, description="文件名字")
    jobID = fields.CharField(max_length=50, null=False, description="任务UUID")
    jobStatus = fields.CharField(max_length=50, null=False, description="任务状态")
    userId = fields.CharField(max_length=50, null=False, description="用户ID")
    uploadUrl = fields.CharField(
        max_length=10000, null=False, description="文件URL list")
    local =  fields.CharField(max_length=50, null=False, description="所属服务器")
