#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: soliva
@Site:
@file: python_pipe_temp.py
@time: 2022/11/23
@desc:
'''
import sys,os,io
import argparse
from signal import signal, SIGPIPE, SIG_DFL

import numpy as np

signal(SIGPIPE, SIG_DFL)
import pandas as pd

def read_vcf(path):
    with open(path, 'r') as f:
        lines = [l for l in f if not l.startswith('##')]
    return pd.read_csv(
        io.StringIO(''.join(lines)),
        dtype={'#CHROM': str, 'POS': int, 'ID': str, 'REF': str, 'ALT': str,
               'QUAL': str, 'FILTER': str, 'INFO': str},
        sep='\t'
    ).rename(columns={'#CHROM': 'CHROM'})




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hsub parser')
    parser.add_argument('input', help='input file 可以使用管道,也可以使用使用 code input_file' ,nargs='?')
    parser.add_argument('-o',"--output", help='output file ')
    args = parser.parse_args()

    if args.input is not  None:
        input_file = args.input
    else:
        input_file  = '/dev/stdin'

    global header
    with open(input_file) as f:
        for line in f.readlines():
            if line.startswith('##INFO=<ID=CSQ'):
                header = line.split('Format:')[1][:-2].split('|')
                break


    def CSQ_read(x):
        try:
            return x["INFO"].split('CSQ=')[1].split(';')[0].split(',')[0]
        except:
            return np.nan

    data = read_vcf(input_file)
    print(data)
    info = data.apply(CSQ_read, axis=1).str.split("|", expand=True)
    info.columns=header
    data.join(info).to_csv(args.output)


sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()