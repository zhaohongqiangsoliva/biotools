#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: soliva
@Site:
@file: python_pipe_temp.py
@time: 2022/11/23
@desc:
'''
import sys, os
import argparse
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)





if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hsub parser')
    parser.add_argument('input', help='input file 可以使用管道,也可以使用使用 Hsub input_file' ,nargs='?')
    args = parser.parse_args()
    import os
    import csv

    # 获取当前目录下的文件列表
    file_list = os.listdir()

    # CSV文件路径和名称
    csv_file = "sample.csv"

    # 定义CSV文件的列名
    fieldnames = ["patient", "sample", "lane", "fastq1", "fastq2"]

    # 打开CSV文件，并写入列名
    with open(csv_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        import os
        import csv
        import re

        # 获取当前目录下的文件列表
        file_list = [d for d in os.listdir() if os.path.isdir(d)]
        print(file_list)

        # CSV文件路径和名称
        csv_file = "data.csv"

        # 定义CSV文件的列名
        fieldnames = ["patient", "sample", "lane", "fastq1", "fastq2"]

        # 打开CSV文件，并写入列名
        with open(csv_file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            # 遍历文件列表
            for index, file_name in enumerate(file_list, start=1):
                # 提取目录序号
                directory_number = index

                # 提取目录名称
                directory_name = file_name



                # 提取目录中的fastq1和fastq2文件名
                directory_path = os.path.abspath(directory_name)
                fastq_files = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if
                               f.endswith("fq.gz")]
                fastq_files.sort()

                if len(fastq_files) >= 2:
                    fastq1 = fastq_files[0]
                    fastq2 = fastq_files[1]
                    # 提取lane号
                    lane = "lane_"+str(index)

                    # 将数据写入CSV文件
                    writer.writerow({
                        "patient": directory_number,
                        "sample": directory_name,
                        "lane": lane,
                        "fastq1": fastq1,
                        "fastq2": fastq2
                    })
                elif len(fastq_files) >=3:
                    fastq3 = fastq_files[2]
                    fastq4 = fastq_files[3]
                    lane2 = "lane_"+str(index+1)

                    writer.writerow({
                        "patient": directory_number,
                        "sample": directory_name,
                        "lane": lane2,
                        "fastq1": fastq3,
                        "fastq2": fastq4
                    })
        print("CSV文件已生成。")






sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()