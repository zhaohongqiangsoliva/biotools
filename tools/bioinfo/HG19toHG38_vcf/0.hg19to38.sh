seq 1 1 22 >chr.sh
echo X >> chr.sh
echo Y >> chr.sh
input_name=$1
parallel -q -j 10 hrun '
CrossMap.py vcf
      /data/reference/liftover_ref/hg19ToHg38.over.chain
      ${input_name}.vcf.gz
      /data/reference/update_gatk_v0/Homo_sapiens_assembly38.fasta
      lifted_over_${input_name}_chr{}.vcf
&&
bcftools sort lifted_over_${input_name}_chr{}.vcf -O z
-o lifted_over_sort_${input_name}_chr{}.vcf.gz
&&
bcftools index -t lifted_over_sort_${input_name}_chr{}.vcf.gz


' :::: chr.sh