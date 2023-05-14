module add apps/GATK/4.1.2.0
fasta=/work/share/ac7m4df1o5/data/ref/gatk_bundle_hg38/data/Homo_sapiens_assembly38.fasta
output_name=$1


ls *g.vcf.gz|awk 'BEGIN{print "'"gatk CombineGVCFs -R $fasta "'"  "\\"  ;} {print "-V " ,$0" \\" } END{ print "'"-O 1.${output_name}.g.vcf.gz"'" }'|bash



#GVCF Combine
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
