seq 1 1 22 >chr.sh
echo X >> chr.sh
echo Y >> chr.sh
parallel -q -j 10 hrun '
CrossMap.py vcf
      /data/reference/liftover_ref/hg19ToHg38.over.chain
      snp.{}.vcf.gz
      /data/reference/update_gatk_v0/Homo_sapiens_assembly38.fasta

      lifted_over_snp_chr{}.vcf
&&
bgzip lifted_over_indel_chr{}.vcf
&&
bcftools index -t lifted_over_indel_chr{}.vcf.gz


' :::: chr.sh