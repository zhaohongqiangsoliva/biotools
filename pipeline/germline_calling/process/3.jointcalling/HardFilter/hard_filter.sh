#export PATH=/work/share/ac7m4df1o5/zhaohq/bio/bin:$PATH
# SNP 过滤
reference=$1
fasta=${reference}/Homo_sapiens_assembly38.fasta
output_name=$2
site_vcf=${reference}/1000G_phase3_v4_20130502.sites.hg38.vcf


gatk SelectVariants \
     -R ${fasta} \
     -V 2.${output_name}.vcf.gz \
     --select-type-to-include SNP \
     -O 3.${output_name}.raw_snps.vcf.gz
# select Indel
gatk SelectVariants \
     -R ${fasta} \
     -V 2.${output_name}.vcf.gz \
     --select-type-to-include INDEL \
     -O 3.${output_name}.raw_indels.vcf.gz

gatk VariantFiltration \
   -R ${fasta} \
   -V 3.${output_name}.raw_snps.vcf.gz \
   -O 4.${output_name}.filtered_snps.vcf.gz \
    -filter "QD < 2.0" --filter-name "QD2" \
    -filter "QUAL < 30.0" --filter-name "QUAL30" \
    -filter "SOR > 3.0" --filter-name "SOR3" \
    -filter "FS > 60.0" --filter-name "FS60" \
    -filter "MQ < 40.0" --filter-name "MQ40" \
    -filter "MQRankSum < -12.5" --filter-name "MQRankSum-12.5" \
    -filter "ReadPosRankSum < -8.0" --filter-name "ReadPosRankSum-8" \

# 满足表达式的变异将被过滤
# filter expressions 和 filter names 之间必须一一对应
# 列出多个过滤表达式和对应的名称
# --filter-name One --filter-expression "X < 1" --filter-name Two --filter-expression "X > 2"
#
# Indel 过滤
gatk VariantFiltration \
   -R ${fasta} \
   -V 3.${output_name}.raw_indels.vcf.gz \
   -O 4.${output_name}.filtered_indels.vcf.gz \
       -filter "QD < 2.0" --filter-name "QD2" \
    -filter "QUAL < 30.0" --filter-name "QUAL30" \
    -filter "FS > 200.0" --filter-name "FS200" \
    -filter "ReadPosRankSum < -20.0" --filter-name "ReadPosRankSum-20" \


##merge indel with snp
 gatk MergeVcfs -I 4.${output_name}.filtered_indels.vcf.gz -I 4.${output_name}.filtered_snps.vcf.gz  -O 5.${output_name}.merge.filter.snps.indels.genotype.vcf.gz

gatk  CalculateGenotypePosteriors \
 -V 5.${output_name}.merge.filter.snps.indels.genotype.vcf.gz \
 -supporting $site_vcf \
 -O 6.${output_name}.SUPsite.snps.indels.genotype.vcf.gz

gatk VariantFiltration  \
 -V 6.${output_name}.SUPsite.snps.indels.genotype.vcf.gz \
 --genotype-filter-expression "GQ < 20" --genotype-filter-name "GQ20" \
 -O 7.${output_name}.genotype_filter.SUPsite.snps.indels.genotype.vcf

bcftools filter -s GQ20 -e "FORMAT/FT[*]!=''" -O z 7.${output_name}.genotype_filter.SUPsite.snps.indels.genotype.vcf.gz \
  > 8.${output_name}.GQfilter.genotype_filter.SUPsite.snps.indels.genotype.vcf



### select variants pass snp with indel
 gatk SelectVariants \
  -R ${fasta} \
  -V 8.${output_name}.GQfilter.genotype_filter.SUPsite.snps.indels.genotype.vcf.gz \
  -O 9.${output_name}.pass.HFILTER.vcf.gz \
  -select "vc.isNotFiltered()"

###bcftools norm with del multiallelics
bcftools norm -m-both -O z -o 10.${output_name}.multiallelics.pass.HFILTER.vcf.gz 9.${output_name}.pass.HFILTER.vcf.gz
bcftools norm -f ${fasta} -O z -o 11.${output_name}.left.multiallelics.pass.HFILTER.vcf.gz 10.${output_name}.multiallelics.pass.HFILTER.vcf.gz