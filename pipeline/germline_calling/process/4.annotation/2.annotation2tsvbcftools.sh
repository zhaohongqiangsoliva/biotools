#!/bin/bash
#$1 input annotation vcf file
#$2 out put format tsv file

echo "CHROM-POS-REF-ALT\t$(bcftools +split-vep -l $1 | cut -f 2 | tr '\n' '\t' | sed 's/\t$//')\tFORMAT\t$(bcftools query -l $1 | awk '{printf("%s\t",$1);} END{printf("\n");}')" >$2
bcftools +split-vep -f '%CHROM-%POS-%REF-%ALT\t%CSQ\t%FORMAT\n' -d -A tab $1 >> $2