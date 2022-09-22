#!/bin/bash
usage() { echo -e "Usage: $0 [-s <string>] [-p <string>] \ncreate template for python -s new a script -p is new a project  " 1>&2; exit 1; }

while getopts ":s:p:" o; do
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
                mkdir -pv ${p} ${p}/{bin,data,Script,note,process/log}

                touch ${p}/process/{main.sh,main.py}
            fi
            ;;
        x)
            cat Extarc/extarc.sh >> ~/.bashrc
            
            ;;
        *)
            usage
            ;;
    esac
done
shift $((OPTIND-1))

if [ -z "${s}" ] && [ -z "${p}" ]; then
    usage
fi