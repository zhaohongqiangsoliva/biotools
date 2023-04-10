#!/bin/bash
bed=$1
bam=$2
out=$3

#bampath /biocluster/data/biobk/user_test/zhaohongqiang/work_space/Statistical_sample_info/bam/W057002T_rmdup.bam
samtools view -H ${bam} >${out}/${bam##*/}_Intervals

awk 'OFS="\t"{$4="+";$5=$1":"$2"-"$3;print $1,$2,$3,$4,$5}' ${bed} >>${out}/${bam##*/}_Intervals

java -jar -Xmx3g ~/software/picard/share/picard-2.18.29-0/picard.jar CollectHsMetrics\
 I=${bam}\
 o=${out}/CalculateHSmetrics \
 R=/biocluster/data/bioexec/database/genome/Homo_sapiens_assembly19/v1/Homo_sapiens_assembly19.fasta \
 TI=${out}/${bam##*/}_Intervals \
 BI=${out}/${bam##*/}_Intervals  \
 VALIDATION_STRINGENCY=SILENT \
 PER_TARGET_COVERAGE=${out}/picard.${bam##*/}.bed
