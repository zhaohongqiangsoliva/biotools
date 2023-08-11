#!/usr/bin/env bash

parallel -q -j10 hrun '
sh /disk/tools/syncthing/ucloud/biotools/tools/bioinfo/VcfAddChr/VCF_Add_chr.sh 
qc.all.chr{}.vcf.gz 
qc.all.chr{}_addchr.vcf.gz

' ::: $(seq 22)