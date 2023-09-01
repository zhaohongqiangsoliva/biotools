#!/usr/bin/env bash

seq 22 > chr.sh
prefix=$1

echo "input out name:$prefix"

mkdir -p tmp/plink_merge
mkdir -p data/QC/merge/
##################### Change format to pgen and merge 
parallel -j 1 -q hrun  "

echo '{} start running'

&&

plink2 
--vcf data/QC/{}_geno.vcf.gz 
--vcf-half-call m 
--make-pgen 
--out tmp/plink_merge/{}
" :::: chr.sh |parallel -j 22 

cat chr.sh |awk '{print "tmp/plink_merge/"$1}' > temp.txt
plink2 --pmerge-list temp.txt --make-pgen --out data/QC/merge/$prefix
