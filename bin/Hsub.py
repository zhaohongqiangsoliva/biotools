# !/usr/bin/env python3
# coding: utf-8
"""

    Qsub helper for The Univa Grid Engine (UGE) at Broad.
    @Author: wavefancy@gmail.com

    Usage:
        qsubHelper.py [-t int] [-m int] [-c int] [-n string] [-l int] [-p txt]
        qsubHelper.py -h | --help | -v | --version  | --format

    Notes:
        1. Read command line from stdin, and output results to stdout.
        2. See example by -f.

    Options:
        -t int        Set the running hours for the jobs, default null.
        -c int        设置总任务核心数量,slurm内的参数为 n/ntask 这个参数的意思还包括当前能跑的任务数量限制,比如我投递1000个任务,-c设置为 5 那么我会用顺序投递5个任务5-5-5-5-5的方式去跑任务
        -m str       Set the memory size, default 2G. Default unit is G设置内存大小默认为2G 默认单位为G
                            如果需要详细设置内存以数字+M为结尾 例如:100M
                         The actual memory loaded is [-c] * [-m], also depending
                         on the number of cpus requested.
        -n string     Set job name, default 'name'.
        -p str        Set the partition name, default: wzhcexclu06, wzhcexclu06|wzhcnormal|wzhdnormal
        -h --help     Show this screen.
        -l int        Line Num
        -v --version  Show version.
        --format   Show input/output file format example.

"""
import sys, os
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL

signal(SIGPIPE, SIG_DFL)


def ShowFormat():
    '''Input File format example:'''
    print('''
# Input
------------------------
line1
line2

#output: -t 10 -m 5 -c 3 -n test
------------------------
qsub -cwd -j y -l h_rt=10:0:0 -l h_vmem=5g -pe smp 3 -binding linear:3 -N test_1 -b y 'line1'
qsub -cwd -j y -l h_rt=10:0:0 -l h_vmem=5g -pe smp 3 -binding linear:3 -N test_2 -b y 'line2'
    ''');


def self_Node_Compute() -> list:
    '''
    sinfo 获取独占节点 cpu 和内存状态 返回参数上限 cpu 和内存：[cpu,mem]
    '''
    import subprocess as sp
    cmd = """sinfo  -p wzhcexclu06  -o  "%P %m %O %C" """
    input_option = sp.getoutput(cmd).split(" ")
    mem, cpu_load, cpu_A, cpu_I, cpu_T = input_option[4], input_option[5], input_option[6].split("/")[0], \
                                         input_option[6].split("/")[1], input_option[6].split("/")[3]
    return (mem, cpu_load, cpu_A, cpu_I, cpu_T)


def autoOption(input_file: str, ) -> str:
    '''
    par:input_file
    fun:
        自动查询脚本里是否有 -n 参数，
        同时查询slurm独立节点是否有空闲,根据空闲数量已经任务数量计算需要的cpu 和 内存

    '''
    mem, cpu_load, cpu_A, cpu_I, cpu_T = self_Node_Compute()
    for _l in input_file:
        pass

def seff_Estimated(job_id):
    import subprocess as sp
    import re
    cmd = f"""seff {job_id} """
    input_option = sp.getoutput(cmd)
    cpu = 0
    mem = 0
    for i in input_option:
        if "Cores per node" in i :
            cpu = i.split(":")[-1]
        if "CPU Efficiency" in i :
            cpu_eff = re.findall(":.*%",i)
            if cpu_eff>70:
                cpu = cpu
            else:
                #10 = 10 -3
                cpu += cpu  - int(cpu /3)
        if "Memory Utilized" in i :
            mem = i.split(":")[-1]
        if "Memory Efficiency" in i:
            mem_eff = re.findall(":.*%", i)
            if mem_eff>70:
                mem = mem
            else:
                #10 = 10 -3
                mem += mem  - int(mem /3)

    return (mem, cpu )







if __name__ == '__main__':
    self_Node_Compute()

#     args = docopt(__doc__, version='1.2')
#     #print(args)

#     if(args['--format']):
#         ShowFormat()
#         sys.exit(-1)

#     N_CPU  = args['-c'] if args['-c'] else '2'
#     N_MEM  = args['-m'] if args['-m'] else '2G'
#     if N_MEM[-1].isdigit():
#         N_MEM += 'G'
#     N_HOUR = args['-t'] if args['-t'] else '2'
#     N_NAME = args['-n'] if args['-n'] else 'name'
#     N_LINE = args['-l'] if args['-l'] else '1'

#     partiton = args['-p'] if args['-p'] else 'wzhcexclu06'

#     temp = 0
#     for line in sys.stdin:
#         line = line.strip()
#         if line:
#             if temp % int(N_LINE) == 0 :
#                 Num = temp % int(N_LINE)
#                 fn = "%s_%d.bash"%(N_NAME, Num)
#                 with open(fn,'w') as ofile:
#                     ofile.write('%s\n'%(line))

#             else:
#                 ofile.write('%s\n'%(line))
# #                temp +=1
#             out = 'sbatch --nodes=1 --ntasks-per-node=1 --time=%s:0:0 --mem=%s --cpus-per-task=%s -e %s.err -o %s.out  --job-name="%s_%d" -p %s  -l %s  "%s" %s \n'%(N_HOUR,N_MEM,N_CPU,N_NAME+'_'+str(temp),N_NAME+'_'+str(temp),N_NAME,temp,partiton,N_LINE,fn)
#             temp += 1
#             sys.stdout.write(out)

# sys.stdout.flush()
# sys.stdout.close()
# sys.stderr.flush()
# sys.stderr.close()
