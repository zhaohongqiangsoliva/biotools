#sh 3.fastq2ubam.sh <json file>
cromshell-alpha submit /work/share/ac7m4df1o5/bin/cromwell/1_pipeline/fastq2ubam/seq-format-conversion-master/paired-fastq-to-unmapped-bam.wdl $i/*.clean.fq.gz.fq2ubam.json -op $i/options.json -n
