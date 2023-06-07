#!/bin/bash
usage() { echo -e "Usage: $0 [-s <string>] [-p <string>] [-x <string>] \ncreate template for python -s new a script -p is new a project  " 1>&2; exit 1; }

while getopts ":xs:p:" o; do
    case "${o}" in
        s)
                s=${OPTARG}
                if [ -f "${s}" ]; then
                echo ${s} '文件已经存在，不能重复创建'
                else 
                echo '
tempplate for detial
@Author:zhaohq 
@Email:zhaohongqiangsoliva@gmail.com
Usage:
    ${s}.py [--mindp int]
    VCFDPFilter.py -h | --help | -e | --example |
Notes:
    notes detial 
Options:
    -参数 --参数     Explanation
import sys
from docopt import docopt
                ' >> ${s}.py
                echo $1 '文件创建成功'
                fi
            ;;
        p)
            p=${OPTARG}
            if [ -d "${p}" ]; 
            then
                echo "${p} project already exists"
            else    
                # 获取当前日期
                current_date=$(date +%Y-%m-%d)

                # 创建目录函数
                create_directory() {
                    directory=$1
                    if [ ! -d "$directory" ]; then
                        mkdir -p "$directory"
                        echo "Created directory: $directory"
                    else
                        echo "Directory already exists: $directory"
                    fi
                }

                # 创建 data 目录及子目录
                create_directory "${p}/data/01_raw/$current_date"
                create_directory "${p}/data/02_processed/$current_date"

                # 创建 code 目录及子目录
                create_directory "${p}/code/01_preprocessing"
                create_directory "${p}/code/02_analysis"
                create_directory "${p}/code/03_models"
                create_directory "${p}/code/04_evaluation"

                # 创建 experiments 目录及子目录
                create_directory "${p}/experiments/01_$current_date"_experiment1
                create_directory "${p}/experiments/02_$current_date"_experiment2
                create_directory "${p}/experiments/03_$current_date"_experiment3

                # 创建 results 目录及子目录
                create_directory "${p}/results/01_$current_date"_experiment1
                create_directory "${p}/results/02_$current_date"_experiment2
                create_directory "${p}/results/03_$current_date"_experiment3

                # 创建 documentation 目录及子目录
                create_directory "${p}/documentation/paper/$current_date"

                echo "Directory structure created successfully!"
            fi
            ;;
        x)  
            SCRIPT_DIR=$(cd $(dirname $(readlink -f ${BASH_SOURCE[0]})); pwd)
            echo ${SCRIPT_DIR}
            cat ${SCRIPT_DIR}/Extract//extract.sh >> ~/.bashrc
            #cat ${SCRIPT_DIR}/Extract//extract.sh >> ~/.zshrc
            echo "PATH=${SCRIPT_DIR}/bin:\$PATH" >> ~/.zshrc
            echo "PATH=${SCRIPT_DIR}/bin:\$PATH" >> ~/.bashrc
            echo "adding extarc to bash and zsh ${shell}"
            ;;
        *)
            usage
            ;;
    esac
done
shift $((OPTIND-1))

if [ -z "${s}" ] && [ -z "${p}" ] && [ -z "${x}" ]; then
    usage
fi
