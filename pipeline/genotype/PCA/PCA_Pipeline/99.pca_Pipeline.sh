#!/usr/bin/env bash

### tips Note
#1.all vcf file need normal    
#bcftools norm -m-both -O z -o rawdata/sedID_1k_institute_QC/1k_institute_QC_setID_MULT.vcf.gz rawdata/sedID_1k_institute_QC/1k_institute_QC_setID_resetHeader.vcf.gz

SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)

prefix_1=$1
prefix_2=$2
#check tools
ls "$SHELL_FOLDER"/PCAKIN_1KG/mergeBedPlink.sh
which CheckDuplicateByKey.py
seq 1 22 >chr.sh
# mkdir -p rawdata/sedID_{${prefix_1},${prefix_2}}
# mkdir -p rawdata/bed_{${prefix_2},${prefix_2}}


############# please !!!!!! Manual Run vcf2bed
#1.DATA Format and QC
#bash "$SHELL_FOLDER"/1.format2bed.sh "${prefix_1}" "${prefix_2}"


#pca pipeline


#2.merge bed

mkdir -p result/merge
mkdir -p result/QC
mkdir -p result/LDprune
mkdir -p result/PCA/
sh ${SHELL_FOLDER}/2.bedMerge.sh "${prefix_1}" "${prefix_2}"


#3.QC
echo "QC start"
sh ${SHELL_FOLDER}/3.QC.sh |parallel -j 22 
echo "QC done"




#4.mergeCHR
echo "mergeCHR start"
sh ${SHELL_FOLDER}/4.mergeChr.sh |bash
echo "mergeCHR done"


#4.LDprune.sh
echo "LD prune start"
sh ${SHELL_FOLDER}/5.LDprune.sh|bash
echo "LD prune done"


#6.PCA
sh ${SHELL_FOLDER}/6.pcakin.plink.sh