
# using annovar annotation hg18 rsid to chr pos ref alt
./annotate_variation.pl -buildver hg18 -downdb -webfrom annovar snp128 humandb/
/data/reference/annotation/annovar/annovar/convert2annovar.pl -format rsid  (cat test.file|wcut -f 1 ) -dbsnpfile /data/reference/annotation/annovar/annovar/humandb/hg18_snp128.txt > snplist.avinput



