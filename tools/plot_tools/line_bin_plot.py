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
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)


sns.lineplot(x=x,y=k1,linestyle='--',label="TOPMAD")
sns.lineplot(x=x,y=k2,linestyle='-',label="BIG_pipeline")
plt.xlabel("Allele Frequency")#横坐标名字
plt.ylabel("R2")#纵坐标名字
plt.legend(loc = "best")#图例
x1=[0.01, 0.05, 0.2, 0.5, 1, 2, 5, 10, 20, 50]
plt.ylim(0,1)
plt.xticks(x,x1)
plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hsub parser')
    parser.add_argument('input', help='input file 可以使用管道,也可以使用使用 Hsub input_file' ,nargs='?')
    parser.add_argument('-bin', dest="bin", help='bin file',)
    args = parser.parse_args()

    if args.input is not  None:
        input_file = args.input
    else:
        input_file  = '/dev/stdin'





sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()



