#!/usr/bin/env bash
#################### dbGaP data：/data/share/wangmx_human/projects/dbgapCAD/



seq 22 > chr.sh
####
input=$1
#/data/reference/update_gatk_v0/
reference_dir=$2
maxdepth=$3
mkdir -p logging

parallel -j 10 -q hrun "
#fillter pass and missing in FILLTER
bcftools view -f 'PASS,.' "${input}"{}.vcf.*
|bcftools norm --fasta-ref ${reference_dir}/Homo_sapiens_assembly38.fasta
--multiallelics 
-both   -Ov
| VCFDPFilter.py --mindp 5 --maxdp ${maxdepth} 2>logging/chr{}_DPFilter.log
| VCFGQFilter.py --mingq 20  2>logging/chr{}_GQFilter.log
| VCFHETMinorReadsRatioFilter.py -c 0.2  2>logging/chr{}_HETMinorReadsRatioFilter.log
| VCFHOMOMinorReadsRatioFilter.py -c 0.1  2>logging/chr{}_HETMinorReadsRatioFilter.log
| VCFSiteMissingFilter.py -m 0.5  2>logging/chr{}_SiteMissing.log
| VCFreFORMATGeno.py -t GT  2>logging/chr{}_reFORMATGeno.log
| VCFSetID.py  
| bgzip > data/QC/{}_geno.vcf.gz 
" :::: chr.sh 