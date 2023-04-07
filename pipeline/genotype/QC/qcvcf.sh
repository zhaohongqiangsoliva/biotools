hrun "
#bcftools filter -Ov -i '%QUAL!=Infinity' -O z -o tmp/snp.{}_fillter.vcf.gz  tmp/snp.{}.vcf.gz
#sh bin/vcfchrom_add_chr.sh  tmp/snp.{}_fillter.vcf.gz tmp/snp.{}_fillter_addchr.vcf.gz
#&& bcftools norm
#--fasta-ref /p300s/wangmx_group/zhaohq/work_space/5_project/ref/gcp-broad-references/gatk_bundle_hg38/V0/Homo_sapiens_assembly38.fasta
#-m-both  tmp/snp.{}_fillter_addchr.vcf.gz
zcat rawdata/huangxt_lifted_over.vcf.gz |python bin/VCF_filter/VCFDPFilter.py --mindp 5
#|python bin/VCF_filter/VCFGQFilter.py --mingq 20
#|python bin/VCF_filter/VCFHETMinorReadsRatioFilter.py -c 0.2
#|python bin/VCF_filter/VCFHOMOMinorReadsRatioFilter.py -c 0.1
#|python bin/VCF_filter/VCFSiteMissingFilter.py -m 0.3
#|python bin/VCF_filter/VCFreFORMATGeno.py -t GT
python bin/VCF_filter/VCFSetID.py
|bgzip > rawdata/huangxt_lifted_over_QC.vcf.gz
"
