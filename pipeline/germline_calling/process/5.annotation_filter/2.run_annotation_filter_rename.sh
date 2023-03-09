input=$1
output=$2
rename=$3
echo "cat ${input}|python bin/5.annotation_filter/1.annotation_filter.py -o ${output} -re '$(bcftools query -l ${rename} | awk '{printf("%s\t",$1);} END{printf("\n");}')' "|bash