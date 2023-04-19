#!/bin/bash
SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)
inputs=$1
output_name=$2
ped=$3
annotation=/data/reference/annotation

hrun "
sh ${SHELL_FOLDER}/1.docker_vep_annotation.sh
${inputs}
2-1.annotation_${output_name}.vcf.gz
${annotation}
&&
sh 2.annotation2tsvbcftools.sh
2-1.annotation_${output_name}.vcf.gz
2-2.annotation_${output_name}.tsv
&&
bgzip 2-2.annotation_${output_name}.tsv
&&

zcat 2-2.annotation_${output_name}.tsv.gz
|sh ${SHELL_FOLDER}/1.vepTsvGnomADFilter.py
-H |bgzip > 2-3.annotation_${output_name}_filter_by_gnomad.tsv.gz
&&

zcat 2-3.annotation_${output_name}_filter_by_gnomad.tsv.gz
|python 2.vep_Pathogenic_fillter.py -ped ${ped}
-o 2-4.annotation_${output_name}_pathogenic.csv

"