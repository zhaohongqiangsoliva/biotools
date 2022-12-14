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

    if args.input is not  None:
        pass
    else:
        pass





sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()