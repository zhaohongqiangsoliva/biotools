seq 1 22 >chr.sh
input=$1
output=$2
parallel -j10 -q hrun "
bcftools view ${input}
 --regions chr{}
 -o ${output} -Oz
" :::: chr.sh