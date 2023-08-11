#!/usr/bin/env bash
SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)

prefix_1=$1
prefix_2=$2
mkdir -p result/merge
mkdir -p result/QC
mkdir -p result/LDprune
(parallel -j 1 -q wecho "
   sh $SHELL_FOLDER/../PCAKIN_1KG/mergeBedPlink.sh
        result/merge/merged.chr{}
        rawdata/bed_${prefix_1}/${prefix_1}_{}
        rawdata/bed_${prefix_2}/${prefix_2}_{}
        {}
    | bash
" :::: chr.sh)|parallel -j 22