#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: soliva
@Site:
@file: Hcat.py
@time: 2022/11/23
@desc:
format Hcat "
            command 1
            |command 2
            |command 3
"
'''
import sys, os
import argparse
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)





if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hsub parser')
    parser.add_argument('input', help='input file or Hsub input_file' ,nargs='?')
    args = parser.parse_args()

    if args.input is not  None:
        input_file = args.input
    else:
        input_file  = '/dev/stdin'





sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()