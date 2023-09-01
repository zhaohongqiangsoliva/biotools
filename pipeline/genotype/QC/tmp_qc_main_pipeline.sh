#!/usr/bin/env bash
#################### dbGaP data：/data/share/wangmx_human/projects/dbgapCAD/


####
input=$1

####please input file prefix name like :
#### test.vcf.gz


####

#################### Clean genotype and phenotype (find the phenotype file or read the project report)

#################### Firstly, cleaning chromosome 19 as posotive control.Then clean chromosome 14.

echo "Cleaning chromosome 19 as posotive control.Then clean chromosome 14."
#################### Make sure the version of the genome!!! (38 or 37)

echo "make sure the version of the genome!!! (38 or 37)"
bash /pmaster/chenxingyu/chenxy/one_trick/judge_version/batch_judge_version.sh -f   1kg_HC_sample_china_all_overlap_chr22.vcf.gz -c 1 -p 2 -r 3 -a 4

#################### Make sure "PASS" in vcf 

seq 1 22 > chr.list 
#################### Have a rough idea of the data. Find proper depth cutoff 
### Calculated mean depth
vcftools --gzvcf {1}_v1.vcf.gz --site-mean-depth --out 
### LCR and SDR annotation in /pmaster/zhangrufan/CAD_rare_variants/scrips/
### Find max depth cutoff 
echo "Find max depth cutoff" 


###make logging dir 

mkdir -p logging/


#################### Split, normalize, genotype filter, python scrips : /pmaster/zhangrufan/CAD_rare_variants/scrips/
parallel -j 10 -q hrun "


bcftools norm --fasta-ref GRCh38_full_analysis_set_plus_decoy_hla.fa 
--multiallelics 
-both "${input}"{}.vcf.gz  -Ov
| python3 VCFDPFilter.py --mindp 5 --maxdp 200 2>>logging/{}_error
| python3 VCFGQFilter.py --mingq 20 2>>logging/{}_error 
| python3 VCFHETMinorReadsRatioFilter.py -c 0.2 2>>logging/{}_error 
| python3 VCFHOMOMinorReadsRatioFilter.py -c 0.1 2>>logging/{}_error 
| python3 VCFSiteMissingFilter.py -m 0.5 2>>logging/{}_error 
| python3 VCFreFORMATGeno.py -t GT 2>>logging/{}_error 
| python3 VCFSetID.py 2>>logging/{}_error 
| bgzip > data/QC/{}_geno.vcf.gz " 
:::: seq 1 22 2>>logging/chr1_split.log 


##################### Change format to pgen and merge 
parallel -j 1 -q hrun  "
plink2 
--vcf {}_geno.vcf.gz 
--vcf-half-call m 
--make-pgen 
--out {}
" :::: seq 1 22


# plink2 --pmerge-list /mnt/project/help_files/file_list/chr2_list.txt pfile --pmerge-list-dir /mnt/project/chr2 --make-pgen --out chr2

# ##################### Variants quality control:missingness, hardy
# ### missingness
# plink2 --pfile chr1_all --missing --out chr1
# ### hardy
# plink2 --pfile chr1_vmissing --hardy --out chr1
# ### filter
# plink2 --pfile chr1 --geno 0.1 --hwe 1e-4 --make-pgen --out chr1_hw


# ##################### Sample quality control:missingness, heterozygocity, sex check
# ### heterozygocity, if the data including different lineage, calculate on different subpopulation.
# plink2 --pfile chr1_all --het 
# ### sex check
# plink --bfile ukb23158_cX_b0_v1 --split-x 2781479 155701383 --make-bed --out chrX_split
# plink --bfile chrX_split --indep-pairwise 50 5 0.2 
# plink --bfile chrX_split --exclude plink.prune.out --make-bed --out chrX_prune
# plink --merge-list X_Y_list --set-hh-missing --make-bed --out sex_X_Y
# plink --bfile sex_X_Y --check-sex ycount 0.5 0.5 1 10000 --out sex_0.5
# grep "PROBLEM" sex_0.5.sexcheck | awk'{print $1,$2}'>sex_discrepancy_ID.txt
# ### remove samples which get from above
# plink2 --pfile chr1_all --remove sample_list_file --make-pgen --out chr1_qc
