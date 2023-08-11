seq 1 22 >chr.sh
output=$2
chr=$3
parallel -j10 -q hrun "

bcftools view $1.vcf.gz
 --regions ${chr}{}
 -o ${output}.splitchr.{}.vcf.gz -Oz
" :::: chr.sh