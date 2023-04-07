#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: soliva
@Site:
@file: python_pipe_temp.py
@time: 2022/11/23
@desc:
'''
import sys, os ,re
import argparse
from signal import signal, SIGPIPE, SIG_DFL
import pandas as pd
import numpy as np
import swifter
import io
signal(SIGPIPE, SIG_DFL)

def read_vcf(path):
    '''
    read vcf
    '''
    with open(path, 'r') as f:
        lines = [l for l in f if not l.startswith('##')]
    return pd.read_csv(
        io.StringIO(''.join(lines)),
        dtype={'#CHROM': str, 'POS': int, 'ID': str, 'REF': str, 'ALT': str,
               'QUAL': str, 'FILTER': str, 'INFO': str},
        sep='\t'
    ).rename(columns={'#CHROM': 'CHROM'})


def read_header(vepannotations):

    global header
    with open(vepannotations) as f:
        for line in f.readlines():
            line.strip()
            if line.startswith('##INFO=<ID=CSQ'):
                header = line.split('Format:')[1][:-2].strip().split('|')
                print(header)
    return header
def format_type(lists,df):

    df[lists]=df[lists].replace('.',np.nan).astype(float)
    return df


def find_Pathogenic(df,names):
    '''
    寻找names  病人的 致病区域 ： 1/1 0/1 1/0 1|1 1|0 0|1 出现一次.
    '''
    num = 0
    jude = 0
    for name in names:
        INFO = df[name].split(":")

        if INFO[0] != '.':
            GT = re.split('\||/', INFO[0])
            GT_ref = GT[0]
            GT_alt = GT[1]
            if int(GT_ref) + int(GT_alt) >= 1:
                jude += 1
            else:
                jude += 0

        else:
            num += 1
            jude += 1
    if num == len(names):
        jude = 0
    if jude == len(names):
        return True
    else:
        return False


def splitpathogenic(df,names):
    for name in names:
        INFO = df[name].split(":")
        df[name]=":".join([INFO[0],INFO[1],INFO[2]])
    return df
def Pathogenic(input,output,Pathogenics_name):
    df=pd.read_csv(input)
    sample_name = Pathogenics_name.split()
    print(sample_name)
    df = df.apple(find_Pathogenic,axis=1,names=sample_name)
    df = df.apple(splitpathogenic,axis=1,names=sample_name)
    df.to_csv(output,index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hsub parser')
    parser.add_argument('input', help='input file 可以使用管道,也可以使用使用 Hsub input_file' ,nargs='+')
    parser.add_argument("-o","--output",help="output tsv file")
    parser.add_argument("-pg",dest="pgname",help="Pathogenics name")
    args = parser.parse_args()

    if args.input is not  None:
        input_file = args.input
    else:
        input_file  = '/dev/stdin'
    print(input_file)
    genotype = pd.read_table(input_file[0])

    filter_gnomad = pd.read_table(input_file[1])

    genotype["CHROM-POS-REF-ALT"] = genotype[["#CHROM", "POS", "REF", 'ALT']].astype(str).agg('-'.join, axis=1)
    merge_df = pd.merge(genotype,filter_gnomad)
    sample_name = ['CHROM-POS-REF-ALT','#CandidatesGenotype','MAX_AF',
       'MAX_AF_POPS', 'CLIN_SIG','Consequence', 'IMPACT', 'SYMBOL', 'Gene']

    df_name = list(merge_df.columns)
    for i in sample_name:
        df_name.remove(i)

    df = merge_df[sample_name + df_name]
    df.to_csv(args.output,index=False)


sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
