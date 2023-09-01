zless $1|sed 's/##contig=<ID=chr/##contig=<ID=/g'  | sed 's/^chr//g'  |bgzip > $2


#for i in `seq 1 22`
#do
#echo "chr$i\t$i"
#done > chr.list

#bcftools annotate --rename-chrs chr.list -O z -o topmad_imputed.dose_delchr2.vcf.gz topmad_imputed.dose.vcf.gz