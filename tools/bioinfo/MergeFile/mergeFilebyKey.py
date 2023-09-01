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
from collections import defaultdict
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)


def nest_dict():
    """无限嵌套dict"""
    return defaultdict(nest_dict)


def header_map(input_file):
    with open(input_file) as f:
        for line in f:
            line = line.strip()

            # 检查是否为注释行（以#开头）
            if line.startswith('#'):
                continue  # 如果是注释行，则跳过

            # 非注释行
            header = line.split()  # 将行分割成列名列表
            header_dict = {col: index for index, col in enumerate(header)}
            return (header_dict)  # 处理完第一行后退出循环


def create_nested_dict(mapdict,key, parts,keys_map):
    mapdict[key]=[value for i, value in enumerate(
                parts) if str(i) not in keys_map]
    return mapdict
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hsub parser')

    parser.add_argument('-m2', '--merge2',
                        help='merge2 file')
    parser.add_argument('-m1', '--merge1',
                        help='merge1 file')
    parser.add_argument("-l", "--lkeys", help="key")
    parser.add_argument("-r", "--rkeys", help="replace")
    parser.add_argument("-H", "--header",help="header")
    args = parser.parse_args()

    merge2_file = args.merge2

    merge2_hd = header_map(merge2_file)
    

    # setting input file incloud stdin and args
    if args.merge1 is not None:
        merge1_file = args.merge1
    else:
        merge1_file = '/dev/stdin'

    merge1_hd = header_map(merge1_file)

# if key is not number, mapping to index of header
    lkeys = args.lkeys.split(",")
    if lkeys[0].isdigit():
        lkeys_map = lkeys
    else:

        lkeys_map = [merge1_hd[i] for i in lkeys]
# rkeys of m2 files
    rkeys = args.rkeys.split(",")
    if rkeys[0].isdigit():
        rkeys_map = rkeys
    else:

        rkeys_map = [merge2_hd[i] for i in rkeys]




    mapdict = {}

    with open(merge2_file, 'r') as file:
        for line in file:
            line = line.strip()
            parts = line.split()  # 假设行中的元素由制表符分隔
            parts_key = [parts[int(i)] for i in rkeys_map]
            keys_set = ":".join(parts_key)
            mapdict = create_nested_dict(mapdict ,keys_set, parts,rkeys_map)

           
    #print(mapdict)
    # merge1_hd = header_map(merge1_file)
    with open(merge1_file,"r") as f:
            # 寻找第一行不以#开头的行，将之前的所有行合并为第一行
        for line in f:
            line = line.strip()
            if not line.startswith('#'):
                if args.header:
                    header2  = '\t'.join(args.header.strip().split())
                    header1  = '\t'.join(merge1_hd.keys())
                    sys.stdout.write(header2 + '\t' + header1 + "\n")
                break


        for line in f:
            line = line.strip()
            # print(line)
            # 检查是否为注释行（以#开头）

            if line.startswith('#'):
                sys.stdout.write(line + "\n")
                continue  # 如果是注释行，则跳过

            parts = line.split()
            parts_key = [parts[int(i)] for i in lkeys_map]
            keys_set = ":".join(parts_key)
            if mapdict.get(keys_set) :
                sys.stdout.write("\t".join(mapdict.get(keys_set)) + "\t"+ line + "\n")
            else :
                sys.stderr.write(keys_set+ "\n")

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
