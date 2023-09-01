#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: soliva
@Site: 
@file: python_pipe_temp.py
@time: 2022/11/23
@desc:
'''
import sys
import os
import argparse
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hsub parser')
    parser.add_argument(
        'input', help='input file 可以使用管道,也可以使用使用 Hsub input_file', nargs='?')
    args = parser.parse_args()

    if args.input is not None:
        input_file = args.input
    # else:
        # input_file  = '/dev/stdin'
df = pd.read_table(input_file, comment="#")
Height = df[["chr_name", "chr_position",
             "effect_allele", "other_allele", "effect_weight"]]


def sorts(x):
    allele = [x["effect_allele"], x["other_allele"]]
    allele.sort()
    snpid = "chr"+str(x["chr_name"]) + ":" + \
        str(x["chr_position"])+":"+allele[0]+":"+allele[1]
    return snpid


Height["SNPid"] = Height.apply(sorts, axis=1)
Height.to_csv("./SNPid_beta.txt", index=False, sep="\t")

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
