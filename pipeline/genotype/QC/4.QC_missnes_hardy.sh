#!/usr/bin/env bash

seq 22 > chr.sh
prefix=$1

echo "The output name:$prefix"

mkdir -p tmp/plink_QC_missingness_hardy_hw

mkdir -p data/plink_QC_missingness_hardy_hw/



plink2 --pfile data/QC/merge/$prefix --missing --out tmp/plink_QC_missingness_hardy_hw/1.${prefix}_missingness
### hardy
plink2 --pfile data/QC/merge/$prefix --hardy --out tmp/plink_QC_missingness_hardy_hw/2.${prefix}_hardy
### filter
plink2 --pfile data/QC/merge/$prefix --geno 0.1 --hwe 1e-4 --make-pgen --out tmp/plink_QC_missingness_hardy_hw/3.${prefix}_hw

ln -f tmp/plink_QC_missingness_hardy_hw/3.${prefix}_hw* data/plink_QC_missingness_hardy_hw/


