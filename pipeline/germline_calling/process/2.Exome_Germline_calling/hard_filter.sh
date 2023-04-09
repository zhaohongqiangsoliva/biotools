module add apps/GATK/4.1.2.0
# SNP 过滤
fasta=$1
output_name=$2
site_vcf=$3

gatk VariantFiltration \
   -R ${fasta} \
   -V 3.${output_name}.raw_snps.vcf \
   -O 4.${output_name}.filtered_snps.vcf \
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
   -V 3.${output_name}.raw_indels.vcf \
   -O 4.${output_name}.filtered_indels.vcf \
       -filter "QD < 2.0" --filter-name "QD2" \
    -filter "QUAL < 30.0" --filter-name "QUAL30" \
    -filter "FS > 200.0" --filter-name "FS200" \
    -filter "ReadPosRankSum < -20.0" --filter-name "ReadPosRankSum-20" \


##merge indel with snp
 gatk MergeVcfs -I 4.${output_name}.filtered_indels.vcf -I 4.${output_name}.filtered_snps.vcf  -O 5.${output_name}.merge.filter.snps.indels.genotype.vcf

gatk  CalculateGenotypePosteriors \
 -V 5.${output_name}.merge.filter.snps.indels.genotype.vcf \
 -supporting $site_vcf \
 -O 6.${output_name}.SUPsite.snps.indels.genotype.vcf

gatk VariantFiltration  \
 -V 6.${output_name}.SUPsite.snps.indels.genotype.vcf \
 --genotype-filter-expression "GQ < 20" --genotype-filter-name "GQ20" \
 -O 7.${output_name}.genotype_filter.SUPsite.snps.indels.genotype.vcf

/work/share/ac7m4df1o5/zhaohq/software/conda_env/bin/bcftools filter -s GQ20 -e "FORMAT/FT[*]!=''" 7.${output_name}.genotype_filter.SUPsite.snps.indels.genotype.vcf \
  > 8.${output_name}.GQfilter.genotype_filter.SUPsite.snps.indels.genotype.vcf



### select variants pass snp with indel
 gatk SelectVariants \
  -R ${fasta} \
  -V 8.${output_name}.GQfilter.genotype_filter.SUPsite.snps.indels.genotype.vcf \
  -O 9.${output_name}.pass.HFILTER.vcf \
  -select "vc.isNotFiltered()"