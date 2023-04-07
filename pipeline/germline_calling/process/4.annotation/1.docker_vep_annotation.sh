#docker run -it  -v ${annotation}/vep/vep_data:/opt/vep/.vep -v /data/zhaohq/project/family_WES_JD:/family:rw -v ${annotation}/vep/:/gnomad --privileged=true  ensemblorg/ensembl-vep:release_107.0 vep -i /family/11.family2_CAD.left.multiallelics.pass.HFILTER.vcf --format vcf --everything --allele_number --no_stats --cache --dir /opt/vep/.vep/cache --offline --assembly GRCh38 --fasta /opt/vep/.vep/Homo_sapiens_assembly38.fasta --af_gnomade --af_gnomadg --pubmed --max_af --custom /family/clinvar.vcf.gz,ClinVar,vcf,exact,0,CLNSIG,CLNREVSTAT,CLNDN --vcf -o /family/12.annotation_family2_clinvar.vcf --force_overwrite


input=$1
output=$2
annotation=$3
hrun "
docker run -i
 -v ${annotation}/vep/vep_data:/opt/vep/.vep
  -v ${annotation}/loftee/vep/vep_data:/loftee
  -v `pwd`:/data:rw -v ${annotation}/vep/:/clinvar
  zihhuafang/ensembl_vep_loftee:v107 vep -i /data/${input}
  --format vcf --everything --allele_number --no_stats --cache
  --dir /opt/vep/.vep/cache --offline --assembly GRCh38
  --fasta /opt/vep/.vep/Homo_sapiens_assembly38.fasta
  --af_gnomade --af_gnomadg --pubmed --max_af
  --custom /clinvar/clinvar.vcf.gz,ClinVar,vcf,exact,0,CLNSIG,CLNREVSTAT,CLNDN
  --plugin LoF,loftee_path:/opt/vep/.vep/Plugins/,gerp_bigwig:/loftee/gerp_conservation_scores.homo_sapiens.GRCh38.bw,human_ancestor_fa:/loftee/human_ancestor.fa.gz,conservation_file:/loftee/loftee.sql
   --dir_plugins /opt/vep/.vep/Plugins/  --vcf -o /data/${output} --force_overwrite

"
