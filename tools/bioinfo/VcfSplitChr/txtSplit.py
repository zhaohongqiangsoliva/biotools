#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: soliva
@Site:
@file: python_pipe_temp.py
@time: 2022/11/23
@desc:
'''
import sys, os,re
import argparse
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)





if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hsub parser')
    parser.add_argument('-s',dest="s", help='input file 可以使用管道,也可以使用使用 Hsub input_file' ,nargs='?')
    args = parser.parse_args()
    #print(args)


    start = args.s
    for i in sys.stdin :
        line = i.strip()
        #print(line)
        if re.search(r"^{}\t".format(start),line):
            #print(line)
            sys.stdout.write(line+"\n")


sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
