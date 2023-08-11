#!/usr/bin/env bash
function singleFile(){
        prefix=$1
        #1.resetID
        hrun -s log/1."${prefix}"_resetID.sh "
        zcat ${prefix}.vcf.gz
        
        |VCFSetID.py
        |bgzip > rawdata/sedID_${prefix}/${prefix}_setID.vcf.gz

        " |bash
        


        #2.merge two file
        (parallel -j 10 -q hrun -s log/2."${prefix}"_merge2bed "
        ## split vcf shanghai  normal samples
        

        #&&
        plink --vcf rawdata/sedID_${prefix}/${prefix}_setID_MULT.vcf.gz
        --chr {}
        --make-bed
        --allow-extra-chr
        --out rawdata/bed_${prefix}/${prefix}_{}


        " :::: chr.sh)|parallel -j 22

}

function mulitFile(){
        prefix=$1
        (parallel -j 10 -q hrun -s log/1."${prefix}"_resetID.sh "
         zcat ${prefix}.chr{}.vcf.gz
         |VCFSetID.py
         |bgzip > rawdata/sedID_${prefix}/${prefix}_chr{}_setID.vcf.gz


         " :::: chr.sh)|parallel -j 22
         (parallel -j 10 -q hrun -s log/2."${prefix}"_merge2bed.sh "
         ## split vcf shanghai  normal samples

         #&&
         plink --vcf rawdata/sedID_${prefix}/${prefix}_chr{}_setID.vcf.gz
         --make-bed
         --allow-extra-chr
         --out rawdata/bed_${prefix}/${prefix}_{}


         " :::: chr.sh)|parallel -j 22

}





function Fomart2bed()
{

prefix_1=$1
prefix_2=$2
if [ -f "${prefix_1}".vcf.gz ];then
          
        singleFile "${prefix_1}"
else
        mulitFile "${prefix_1}"
fi

if [ -f "${prefix_2}".vcf.gz ];then
        singleFile "${prefix_2}"

else
        mulitFile "${prefix_2}"
fi
}

Fomart2bed "$1" "$2"