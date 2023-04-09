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

def unfunction(df,names):
    '''
    去除非功能区

    '''
    for name in names:
        df =df[-df["Consequence"].str.contains(name, regex=True)]
    return df
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
def filter(x):

        filter_name = x['MAX_AF_POPS'].split("&")[0]
        if filter_name != '.':
            if float(x[filter_name + "_AF"]) < 0.01:
                return True
            else:
                return False
        else:
            return True

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

def Pathogenic(input,output,rename):
    data=pd.read_table(input)

    df = unfunction(data, ["downstream", "intron", "synonymous", "upstream", "non_coding"])
    df = df[(-df["IMPACT"].str.contains("MODIFIER", regex=True)) & (-df["IMPACT"].str.contains("LOW", regex=True))]
    df=df[df.apply(filter, axis=1)]
    df=unfunction(df,["downstream","intron","synonymous","upstream","non_coding"])
    df =df[(-df["IMPACT"].str.contains("MODIFIER", regex=True) )&( -df["IMPACT"].str.contains("LOW", regex=True))]
    df=df.drop_duplicates(["CHROM-POS-REF-ALT","Consequence"])
    if rename:
        sample_name = rename.split()
        print(sample_name)
        df_name = list(df.columns)
        for i in sample_name:
            df_name.remove(i)

        df=df[sample_name+df_name]
    else:
        pass
    df.to_csv(output,index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hsub parser')
    parser.add_argument('input', help='input file 可以使用管道,也可以使用使用 Hsub input_file' ,nargs='?')
    parser.add_argument("-o","--output",help="output tsv file")
    parser.add_argument("-re",dest="rename",help="resort col names")
    args = parser.parse_args()

    if args.input is not  None:
        input_file = args.input
    else:
        input_file  = '/dev/stdin'
    Pathogenic(input_file,args.output,args.rename)




sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()

