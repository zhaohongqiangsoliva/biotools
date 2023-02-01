#module add apps/GATK/4.1.2.0
export PATH=/work/share/ac7m4df1o5/zhaohq/bio/bin/:$PATH
fasta=/work/share/ac7m4df1o5/data/ref/gatk_bundle_hg38/data/Homo_sapiens_assembly38.fasta
output_name=$1

mkdir tmp
seq 1 22 > list.txt
echo X >>  list.txt
echo Y >>  list.txt
#ls *rb.g.vcf.gz|awk 'BEGIN{print "'"gatk CombineGVCFs -R $fasta "'"  "\\"  ;} {print "-V " ,$0" \\" } END{ print "'"-O 1.${output_name}.g.vcf.gz"'" }'|bash
mapfile=${output_name}.map.file
ls *.g.vcf.gz |awk -F '.' '{print $1"\t"$0}'> ${mapfile}
parallel -j 10 "/work/share/ac7m4df1o5/zhaohq/bio/bin/gatk GenomicsDBImport --sample-name-map  ${mapfile}  --genomicsdb-workspace-path Genomicsdb.{} --intervals chr{} --tmp-dir ./tmp" :::: list.txt

parallel -j 10 "/work/share/ac7m4df1o5/zhaohq/bio/bin/gatk GenotypeGVCFs -R ${fasta}  -V  gendb://Genomicsdb.{} -O ${output_name}{}.vcf -ped ped.file -L chr{} -G StandardAnnotation --only-output-calls-starting-in-intervals --use-new-qual-calculator -D /work/share/ac7m4df1o5/data/ref/gatk_bundle_hg38/data/Homo_sapiens_assembly38.dbsnp138.vcf" :::: list.txt

/work/share/ac7m4df1o5/zhaohq/bio/bin/gatk GatherVcfs `for i in $(cat list.txt);do echo "-I ${output_name}$i.vcf";done` -O 2.${output_name}.vcf
#/work/share/ac7m4df1o5/zhaohq/bio/bin/gatk GenomicsDBImport -V cromwell/outputs/family_calling_map.sample_map --genomicsdb-workspace-path Genomicsdb.{} --intervals chr{} --tmp-dir ./tmp
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
