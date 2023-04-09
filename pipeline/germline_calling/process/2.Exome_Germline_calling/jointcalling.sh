module add apps/GATK/4.1.2.0
fasta=$1
output_name=$2

# GVCF Combine
#gatk CombineGVCFs \
#   -R  /work/share/ac7m4df1o5/data/ref/gatk_bundle_hg38/data/Homo_sapiens_assembly38.fasta \
#  -V  PC01.rb.g.vcf.gz \
#  -V  PC03.rb.g.vcf.gz \
#  -V  PC04.rb.g.vcf.gz \
#  -V  PC05.rb.g.vcf.gz \
#  -V  PC08.rb.g.vcf.gz \
#  -V  PC09.rb.g.vcf.gz \
#  -V  PC10.rb.g.vcf.gz \
#  -V  PC11.rb.g.vcf.gz \
#  -V  PC12.rb.g.vcf.gz \
#  -V  PC13.rb.g.vcf.gz \
#  -V  PC14.rb.g.vcf.gz \
#  -V  PC15.rb.g.vcf.gz \
#  -V  PC16.rb.g.vcf.gz \
#  -V  PC17.rb.g.vcf.gz \
#  -V  PC18.rb.g.vcf.gz \
#  -V  PC19.rb.g.vcf.gz \
#  -V  PC20.rb.g.vcf.gz \
#  -V  PC21.rb.g.vcf.gz \
#  -V  shaoqi.rb.g.vcf.gz \
#  -V  wangqinglan.rb.g.vcf.gz \
#  -O 1.${output_name}.g.vcf.gz


# gvcf joint calling
gatk --java-options "-Xmx4g" GenotypeGVCFs \
   -R ${fasta} \
   -V *${output_name}.g.vcf.gz \
   -O 2.${output_name}.vcf.gz \
   -ped ped.file

## Select Variants
# select SNPs
gatk SelectVariants \
     -R ${fasta} \
     -V 2.${output_name}.vcf.gz \
     --select-type-to-include SNP \
     -O 3.${output_name}.raw_snps.vcf
# select Indel
gatk SelectVariants \
     -R ${fasta} \
     -V 2.${output_name}.vcf.gz \
     --select-type-to-include INDEL \
     -O 3.${output_name}.raw_indels.vcf