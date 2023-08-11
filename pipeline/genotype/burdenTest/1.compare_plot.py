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



def compare_summary(line_list,genelist,col):
        # df = pd.read_csv(csv, compression='gzip')
        #
        # def coun_sample(x):
        #     geno = [sum(map(int, re.split('\||/', i.split(":")[0]))) for i in x if "." not in i.split(":")[0]]
        #     return (sum(i >= 1 for i in geno))
        #
        # #         geno = re.split('\||/',i)
        # #         print(sum(map(int, geno)))
        # ####################################
        # gdf = df.groupby("SYMBOL").count()
        #
        # gene = [i for i in gdf.index
        #         if i in ['PRRT2',
        #                  'TMEM151A',
        #                  'PNKD',
        #                  'CHRNA4',
        #                  'SCN8A',
        #                  'ADCY5',
        #                  'DEPDC5',
        #                  'PDE2A',
        #                  'SLC2A1',
        #                  'KCNA1',
        #
        #                  ]]
        # return gene
        #
        #
        #
        # gene_df = df[df["SYMBOL"].isin(gene)]
        # gene_df["geno_count"] = df[df["SYMBOL"].isin(gene) & df["Consequence"].str.contains("frameshift_variant")].iloc[
        #                         :, 92:].apply(coun_sample, axis=1)
        # ggene_df = gene_df[gene_df["geno_count"] >= 1].groupby("SYMBOL").sum()["geno_count"]
        #
        # return ggene_df

        pass






if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hsub parser')
    parser.add_argument('input', help='input file 可以使用管道,也可以使用使用 Hsub input_file' ,nargs='?')
    parser.add_argument('-g',"--genelist", help='input genelist file as comparison')
    parser.add_argument("-d","--dim",default=",",help="dim separator")
    args = parser.parse_args()

    if args.input is not  None:
        input_file = args.input
    else:
        input_file  = '/dev/stdin'
    gene_list=list()
    with open(args.genelist, 'r') as f:
        gene_list = [i for i in f.read().split('\n') if i != '']
    col = dict()
    with open(input_file, 'r') as f:
        for line in f:
            line=line.strip()
            line_list = line.split(args.dim)

            if line.startswith('CHROM'):
                # first line contains header
                #{'CHROM-POS-REF-ALT': 0, 'Allele': 1, 'Consequence': 2, 'IMPACT': 3, 'SYMBOL': 4 .....}
                col=dict(map(reversed, enumerate(line.split(args.dim))))
                # print(col)
                sys.stdout.write(line+"\n")
            else:
                line_list = line.split(args.dim)
                #print(gene_list,line_list[col['SYMBOL']])
                if line_list[col['SYMBOL']] in gene_list:
                    sys.stdout.write(line + "\n")

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()