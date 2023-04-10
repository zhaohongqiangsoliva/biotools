output=$1
ls *.g.vcf.gz |awk -v name=`pwd` -F '.' '{print $1"\t"name"/"$1".rb.g.vcf.gz"}' >${output}.map