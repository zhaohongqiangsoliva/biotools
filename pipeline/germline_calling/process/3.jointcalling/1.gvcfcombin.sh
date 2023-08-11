#module add apps/GATK/4.1.2.0
#export PATH=/work/share/ac7m4df1o5/zhaohq/bio/bin/:$PATH
reference=$2
fasta=${reference}/Homo_sapiens_assembly38.fasta
output_name=$1
ped=$3
mkdir tmp
seq 1 22 > list.txt
echo X >>  list.txt
echo Y >>  list.txt
#ls *rb.g.vcf.gz|awk 'BEGIN{print "'"gatk CombineGVCFs -R $fasta "'"  "\\"  ;} {print "-V " ,$0" \\" } END{ print "'"-O 1.${output_name}.g.vcf.gz"'" }'|bash
mapfile=${output_name}.map.file

ls *.g.vcf.gz |awk -F '.' '{print $1"\t"$0}'> ${mapfile}
parallel -j 10 "gatk GenomicsDBImport --sample-name-map  ${mapfile}  --genomicsdb-workspace-path Genomicsdb.{} --intervals chr{} --tmp-dir ./tmp" :::: list.txt

if  [ ! -n "$3" ] ;then
    echo "you have not input a ped"
    parallel -j 10 "gatk GenotypeGVCFs -R ${fasta}  -V  gendb://Genomicsdb.{} -O ${output_name}{}.vcf  -L chr{} -G StandardAnnotation --only-output-calls-starting-in-intervals --use-new-qual-calculator -D ${reference}/Homo_sapiens_assembly38.dbsnp138.vcf" :::: list.txt

else
    echo "the input is $3"
    parallel -j 10 "gatk GenotypeGVCFs -R ${fasta}  -V  gendb://Genomicsdb.{} -O ${output_name}{}.vcf -ped $ped -L chr{} -G StandardAnnotation --only-output-calls-starting-in-intervals --use-new-qual-calculator -D ${reference}/Homo_sapiens_assembly38.dbsnp138.vcf" :::: list.txt

fi
#parallel -j 10 "gatk GenotypeGVCFs -R ${fasta}  -V  gendb://Genomicsdb.{} -O ${output_name}{}.vcf -ped $ped -L chr{} -G StandardAnnotation --only-output-calls-starting-in-intervals --use-new-qual-calculator -D ${reference}/Homo_sapiens_assembly38.dbsnp138.vcf" :::: list.txt

gatk GatherVcfs $(for i in $(cat list.txt);do echo "-I ${output_name}$i.vcf";done) -O 2.${output_name}.vcf
bgzip 2.${output_name}.vcf
tabix -f 2.${output_name}.vcf.gz

mv Genomicsdb.* tmp
rm *vcf *vcf.idx
