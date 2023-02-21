site_vcf=/data/reference/gcp-broad-references/gatk_bundle_hg38/update_gatk_v0/1000G_phase3_v4_20130502.sites.hg38.vcf
output_name=$1
fasta=/data/reference/gcp-broad-references/gatk_bundle_hg38/update_gatk_v0/Homo_sapiens_assembly38.fasta
##merge indel with snp
indel=$2
snp=$3

gatk MergeVcfs -I ${indel} -I 4.${snp}  -O 5.${output_name}.merge.filter.snps.indels.genotype.vcf

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

###bcftools norm with del multiallelics
bcftools norm -m-both -o 10.${output_name}.multiallelics.pass.HFILTER.vcf 9.${output_name}.pass.HFILTER.vcf
bcftools norm -f ${fasta} -o 11.${output_name}.left.multiallelics.pass.HFILTER.vcf 10.${output_name}.multiallelics.pass.HFILTER.vcf