

cat $1|awk '{print $1"\t"$2-100"\t"$3+100}' |bedtools merge -i > $2
