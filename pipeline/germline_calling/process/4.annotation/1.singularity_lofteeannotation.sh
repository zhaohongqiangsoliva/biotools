#!/bin/bash
#SBATCH -p wzhcnormal
#SBATCH --cpus-per-task=4




module add apps/singularity/3.7.3
cat 10.family_calling.genotypeFilter.HF.vcf|singularity exec --bind /work/share/ac7m4df1o5/bin/annotation/vep/vep_data:/opt/vep/.vep/ --bind `pwd`:/data /work/share/ac7m4df1o5/bin/annotation/vep/singularity-cache/vep95_loftee:0.2.sif /opt/vep/src/ensembl-vep/vep --format vcf --everything --allele_number --no_stats --cache --dir /opt/vep/.vep/ --offline --minimal --assembly GRCh38 --fasta /opt/vep/.vep/homo_sapiens/95_GRCh38/Homo_sapiens.GRCh38.dna.toplevel.fa.gz --tab --plugin Downstream  --dir_plugins /opt/vep/Plugins/  --fork 4  -o /data/12.annotation_family_calling.genotypeFilter.HF.tsv
