# SNPs VQSR
gatk VariantRecalibrator \
   -R <ucsc.hg3838.fasta> \
   -V <raw_snps.vcf> \
   --resource hapmap,known=false,training=true,truth=true,prior=15.0:hapmap_3.3.hg38.sites.vcf.gz \
   --resource omni,known=false,training=true,truth=false,prior=12.0:1000G_omni2.5.hg38.sites.vcf.gz \
   --resource 1000G,known=false,training=true,truth=false,prior=10.0:1000G_phase1.snps.high_confidence.hg38.vcf.gz \
   --resource dbsnp,known=true,training=false,truth=false,prior=2.0:Homo_sapiens_assembly38.dbsnp138.vcf.gz \
   -an QD -an MQ -an MQRankSum -an ReadPosRankSum -an FS -an SOR \
   -mode SNP \
   -O <snps_recalibrate.recal> \
   --tranches-file <snps_recalibrate.tranches> \
   --rscript-file <snps_recalibrate.plots.R>
gatk ApplyVQSR \
   -R <ucsc.hg38.fasta> \
   -V <raw_snps.vcf> \
   -O <snps_recalibrate.vcf> \
   --truth-sensitivity-filter-level 99.5 \
   --tranches-file <snps_recalibrate.tranches> \
   --recal-file <snps_recalibrate.recal> \
   -mode SNP
##
# Indels VQSR
gatk VariantRecalibrator \
   -R <ucsc.hg38.fasta> \
   -V <raw_indels.vcf> \
   --maxGaussians 4 \
   -resource:mills,known=false,training=true,truth=true,prior=12.0 Mills_and_1000G_gold_standard.indels.hg38.vcf  \
   -resource:dbsnp,known=true,training=false,truth=false,prior=2.0 dbsnp_146.hg38.vcf\
   -an QD -an DP -an FS -an SOR -an ReadPosRankSum -an MQRankSum -an InbreedingCoeff \
   -mode INDEL \
   -O <indels_recalibrate.recal> \
   --tranches-file <indels_recalibrate.tranches> \
   --rscript-file <indels_recalibrate.plots.R>
gatk ApplyVQSR \
   -R <ucsc.hg38.fasta> \
   -V <raw_indels.vcf> \
   -O <indels_recalibrate.vcf> \
   --truth-sensitivity-filter-level 99.0 \
   --tranches-file <indels_recalibrate.tranches> \
   --recal-file <indels_recalibrate.recal> \
   -mode INDEL