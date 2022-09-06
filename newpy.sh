#!/bin/bash
usage() { echo "Usage: $0 [-s <string>] [-p <string>] \n create template for python -s new a script -p is new a project  " 1>&2; exit 1; }

while getopts ":s:p:" o; do
    case "${o}" in
        s)
            s=${OPTARG}
            ;;
        p)
            p=${OPTARG}
            ;;
        *)
            usage
            ;;
    esac
done
shift $((OPTIND-1))

if [ -z "${s}" ] && [ -z "${p}" ]; then
    usage
else

if [ -n "${s}" ] ;then
 if [ -f "${s}" ]; then
 echo ${s} '文件已经存在，不能重复创建'
else 
 echo '
    tempplate for detial
    @Author: zhaohongqiangsoliva@gmail.com

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
fi
if [  -n "${p}" ] ;then
    if [ -d "${p}" ]; 
    then
        echo "${p} project already exists"
    else    
        mkdir -pv ${p} ${p}/{bin,data,Scripy,note,process/log}

        touch ${p}/process/{main.sh,main.py}
    fi
fi


fi
