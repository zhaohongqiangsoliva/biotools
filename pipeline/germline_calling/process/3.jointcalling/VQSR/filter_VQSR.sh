# SNPs VQSR
fasta=/data/reference/gcp-broad-references/gatk_bundle_hg38/update_gatk_v0/Homo_sapiens_assembly38.fasta
raw_snps_vcf=$1
gatk_reference=/data/reference/gcp-broad-references/gatk_bundle_hg38/update_gatk_v0
output=$2

#gatk VariantRecalibrator \
#   -R $fasta \
#   -V $raw_snps_vcf \
#   --resource:hapmap,known=false,training=true,truth=true,prior=15.0 ${gatk_reference}/hapmap_3.3.hg38.vcf.gz \
#   --resource:omni,known=false,training=true,truth=false,prior=12.0 ${gatk_reference}/1000G_omni2.5.hg38.vcf.gz \
#   --resource:1000G,known=false,training=true,truth=false,prior=10.0 ${gatk_reference}/1000G_phase1.snps.high_confidence.hg38.vcf.gz \
#   --resource:dbsnp,known=true,training=false,truth=false,prior=2.0 ${gatk_reference}/Homo_sapiens_assembly38.dbsnp138.vcf.gz \
#   -an QD -an MQ -an MQRankSum -an ReadPosRankSum -an FS -an SOR \
#   -mode SNP \
#   -O ${output}_snps_recalibrate.recal \
#   --tranches-file ${output}_snps_recalibrate.tranches \
#   --rscript-file ${output}_snps_recalibrate.plots.R
#
#gatk ApplyVQSR \
#   -R $fasta \
#   -V $raw_snps_vcf \
#   -O ${output}_snps_recalibrate.vcf \
#   --truth-sensitivity-filter-level 99.5 \
#   --tranches-file ${output}_snps_recalibrate.tranches \
#   --recal-file ${output}_snps_recalibrate.recal \
#   -mode SNP
##
# Indels VQSR
gatk VariantRecalibrator \
   -R $fasta \
   -V $raw_snps_vcf \
     -tranche 100.0 -tranche 99.95 -tranche 99.9 \
  -tranche 99.5 -tranche 99.0 -tranche 97.0 -tranche 96.0 \
  -tranche 95.0 -tranche 94.0 -tranche 93.5 -tranche 93.0 \
  -tranche 92.0 -tranche 91.0 -tranche 90.0 \
   -resource:mills,known=false,training=true,truth=true,prior=12.0 ${gatk_reference}/Mills_and_1000G_gold_standard.indels.hg38.vcf.gz  \
   -resource:dbsnp,known=true,training=false,truth=false,prior=2.0 ${gatk_reference}/gdc/dbsnp_144.hg38.vcf.gz \
   -an QD -an DP -an FS -an SOR -an ReadPosRankSum -an MQRankSum -an InbreedingCoeff \
   -mode INDEL \
   -O ${output}_indels_recalibrate.recal \
   --tranches-file ${output}_indels_recalibrate.tranches \
   --rscript-file ${output}_indels_recalibrate.plots.R
gatk ApplyVQSR \
   -R $fasta \
   -V $raw_snps_vcf \
   -O ${output}_indels_recalibrate.vcf \
   --truth-sensitivity-filter-level 99.0 \
   --tranches-file ${output}_indels_recalibrate.tranches \
   --recal-file ${output}_indels_recalibrate.recal \
   -mode INDEL