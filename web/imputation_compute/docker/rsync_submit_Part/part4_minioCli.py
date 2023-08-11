#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Description:       :
@Date     :2023/07/21 09:25:12
@Author      :soliva
@version      :1.0
'''

from miniopy_async import Minio
from minio.error import S3Error
import os
import glob
import aiohttp


def upload_local_directory_to_minio(local_path, bucket_name, minio_path, client):
    assert os.path.isdir(local_path)
    file_url_list = []
    for local_file in glob.glob(local_path + '/**'):
        # Replace \ with / on Windows
        local_file = local_file.replace(os.sep, "/")
        if not os.path.isfile(local_file):
            ### 递归 异步上传文件
            upload_local_directory_to_minio(
                local_file, bucket_name, minio_path + "/" + os.path.basename(local_file))
        else:
            remote_path = os.path.join(
                minio_path, local_file[1 + len(local_path):])
            remote_path = remote_path.replace(
                os.sep, "/")  # Replace \ with / on Windows
            if  client.fput_object(bucket_name, remote_path, local_file):
                file_url_list.append(remote_path)
    return file_url_list


def upload_to_minio(access_key, secret_key, bucket_name, folder_path, object_path, minio_endpoint):
    try:
        
            # Initialize MinIO client
            minio_client = Minio(
                minio_endpoint,  # MinIO服务器的地址
                access_key=access_key,
                secret_key=secret_key,
                secure=False  # 如果使用HTTP而非HTTPS，请设置为False
            )

            # 确保存储桶存在，如果不存在则创建

            if not minio_client.bucket_exists(bucket_name):
                minio_client.make_bucket(bucket_name)

            # 构建对象名称，包括前缀（模拟文件夹结构）
            # object_name = f"{folder_path}/{file_name}"
            file_url = upload_local_directory_to_minio(
                folder_path, bucket_name, object_path, minio_client)

            # # 构建并返回上传文件的访问路径
            base_url = f"http://{minio_endpoint}"  # MinIO服务器的基本URL

            return [f"{base_url}/{bucket_name}/{i}" for i in file_url]

    except S3Error as e:
        print("Error occurred: ", e)


if __name__ == "__main__":
    object_path = "output/1/project_test"
    bucket_name = "imputation"
    # object_name = "test"  # Name of the object when stored in MinIO
    minio_endpoint = "118.195.223.193:9000"  # For example, "play.minio.io:9000"
    access_key = "JnHKZFBpgwRDVL02AM0h"
    secret_key = "gLWKCG6OvclTHT9vJcc7EZSOCW4V7s0evjqLhG2r"
    folder_path = "/disk/project/imputation/imputation_web/userDATA/1/cromwell/output"
    # file_name = "3341231.dose.vcf.gz"

    uploaded_file_url = upload_to_minio(
        access_key, secret_key, bucket_name, folder_path, object_path, minio_endpoint)
    print("Uploaded File URL:", uploaded_file_url)
