seq 1 22 >chr.sh
parallel -j10 -q hrun "
bcftools view merge-1kg_raw_setID.vcf_addchr.gz
 --regions chr{}
 -o split/merge-1kg_raw_setID.vcf_chr{}.vcf.gz -Oz
" :::: chr.sh