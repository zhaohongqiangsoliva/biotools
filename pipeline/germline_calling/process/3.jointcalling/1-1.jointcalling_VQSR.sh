#!/usr/bin/env bash
reference=$2
outname=$1
SHELL_FOLDER=$(cd "$(dirname "$0")" || exit;pwd)
hrun "
#combin gvcf to vcf file
sh ${SHELL_FOLDER}/1.gvcfcombin.sh
${outname}
${reference}
&&
#using gatk VQSR filter vcf
sh ${SHELL_FOLDER}/VQSR/filter_VQSR.sh
2.${outname}.vcf.gz
${outname}
${reference}

#&&
sh ${SHELL_FOLDER}/3.merge_norm.sh
$outname
2.VQSR_indels_recalibrate.vcf
2.VQSR_snps_recalibrate.vcf
${reference}
"
