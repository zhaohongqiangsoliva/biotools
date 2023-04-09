# !/usr/bin/env python3
# coding: utf-8
"""

"""
import sys, os
import argparse
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)



def self_Node_Compute(p) -> tuple:
    '''
    sinfo 获取独占节点 cpu 和内存状态 返回参数上限 cpu 和内存：[cpu,mem]
    '''
    import subprocess as sp
    cmd = f"""sinfo  -p {p}  -o  "%P %m %O %C" """
    input_option = sp.getoutput(cmd).split(" ")
    mem, cpu_load, cpu_A, cpu_I, cpu_T = input_option[4], input_option[5], input_option[6].split("/")[0], \
                                         input_option[6].split("/")[1], input_option[6].split("/")[3]

    return (mem, cpu_load, cpu_A, cpu_I, cpu_T)


def autoOption(time,
               job_name,
               ntask=8,
               cpu:int = 8,
               mem:int = 16,
               partition:str="wzhcexclu06",
               job_cpu:int=1,
               runs:int=8
               ) -> str :
    '''
    par:input_file
    fun:
        输入cpu 和 mem 同时查询slurm独立节点是否有空闲

    '''
    mem_Q, cpu_load, cpu_A, cpu_I, cpu_T = self_Node_Compute(partition)
    if cpu <int(cpu_I):
        # SBATCH --cpus-per-task={cpu}
        header = f'''\
#!/bin/bash
#SBATCH --time={time}
#SBATCH --job-name={job_name}
#SBATCH -p {partition}
#SBATCH -N 1
#SBATCH -n {ntask}
#SBATCH --mem={mem}

mkdir -p logs
date
srun="srun -N1 -n{job_cpu}"

parallel="parallel --delay .2 -j {runs} --joblog logs/runtask.log --resume"
\n\n$parallel  '''
        return (header)
    else :

        Exception("error cpu is not enough")




def seff_Estimated(job_id:str,p:str) :
    '''
    par:job id
    fun:
        查看过去的任务使用情况，如果大于70%的占用，保持任务不变，如果小于70 减小1/3的核心

    '''
    import subprocess as sp
    import re
    cmd = f"""seff {job_id} """
    input_option = sp.getoutput(cmd)
    cpu = 0
    mem = 0
    print(input_option)
    for info in input_option.split("\n"):
        if "Cores per node" in info :
            cpu = int(info.split(":")[-1])
        if "CPU Efficiency" in info :
            cpu_eff = re.findall("\d.*(?=%)",info)[0]
            if float(cpu_eff)>70:
                cpu = cpu
            else:
                #10 = 10 -3
                cpu += cpu  - int(int(cpu) /3)
        if "Memory Utilized" in info :
            mem = float(re.findall("\d\..*\d", info)[0])
        if "Memory Efficiency" in info:
            mem_eff = re.findall("\d.*(?=%)", info)[0]
            if float(mem_eff)>70:
                mem = mem
            else:
                #10 = 10 -3
                mem += mem  - int(int(mem) / 3)

    mem_old, cpu_load, cpu_A, cpu_I, cpu_T = self_Node_Compute(p)
    print("推荐参数：",int(mem), int(cpu))
    print("目前节点状态：mem_old, cpu_load, cpu_A, cpu_I, cpu_T \n",mem_old, cpu_load, cpu_A, cpu_I, cpu_T )
    return (int(mem), int(cpu))







if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hsub parser')
    parser.add_argument('input', help='input file 可以使用管道cat file |Hsub <options>,也可以使用使用 Hsub input_file <options>' ,nargs='?')
    parser.add_argument('-c',"--CPU", help='CPU cpus-per-task=1  指定每个进程使用核数，不指定默认为8 ',default=8)
    parser.add_argument('-m', "--MEM",help='MEM',default=16000)
    parser.add_argument('-t', "--TIME",help='time',default=30000)
    parser.add_argument('-p', "--partition",help='节点 默认使用独占节点',default="wzhcexclu06")
    parser.add_argument('-n',"--ntask", help="指定总进程数；不使用cpus，可理解为进程数即为核数 (主要使用这个参数) 需计算jobs X runs 如 'jobs x runs = 2 X 8' ntask=16 ",default=8*1)
    parser.add_argument("-j","--jobs",help="任务所需核数，默认为1",default=1)
    parser.add_argument("-r","--runs",help="运行同时并行几个任务，在jobs为1时等于ntask",default=8)
    parser.add_argument("-name","--name",help="任务名称",default="Hsub_submit")
    args = parser.parse_args()
    print(args)
    if args.input is not  None:
        input_file = args.input
    else:
        input_file  = '/dev/stdin'


    with open("submit.sh","w") as f:
        header = autoOption(time=args.TIME,
                           job_name=args.name,
                           ntask=8,
                           cpu= args.CPU,
                           mem=args.MEM,
                           partition=args.partition,
                           job_cpu=args.jobs,
                           runs=args.runs,
                            )
        f.write(header)
        sys.stdout.write(header)
        with open("comlist.sh","w") as f1:
            for _line in open(input_file).readlines():
                _lines = _line.strip()
                out = _lines +"\n"
                #sys.stdout.write(out)
                f1.write(out)

        sys.stdout.write("< comlist.sh")
        sys.stdout.write("date\n")
        f.write("< comlist.sh\n")
        f.write("date\n")

        f.write("wait")

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
