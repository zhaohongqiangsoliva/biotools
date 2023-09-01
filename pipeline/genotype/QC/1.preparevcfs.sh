#!/usr/bin/env bash
prefix=$1
vcfs=$2

mkdir -p tmp/check

echo "#CHROM\tPOS\tFILTER\tGT:DP:GQ:PL" >tmp/check/checklist

bcftools query -f '%CHROM\t%POS\t%FILTER[\t%GT:%DP:%GQ:%PL]\n' "$vcfs" |head -n 10 >>tmp/check/checklist
PREFIX=$prefix
parallel -j 10 -q hrun "

vcftools --gzvcf "${PREFIX}" --site-mean-depth --out tmp/check/{}_mean_depth

" ::: $(seq 22) 