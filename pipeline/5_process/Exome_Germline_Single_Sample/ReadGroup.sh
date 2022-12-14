#if fastq.gz change cat to zcat
header=$(zcat $1 | head -n 1)
fastq1=$(basename $1)
fastq2=$(basename $2)
outputs=$3
ID=$(echo $header | head -n 1 | cut -f 1-3 -d":" | sed 's/@//' | sed 's/:/./g')
PU=$(echo $header | head -n 1 | cut -f 1-4 -d":" | sed 's/@//' | sed 's/:/./g')
SM=$(echo $fastq1|sed "s#.fastq\|.fq\|.fastq.gz\|.fq.gz##g")
LB="$(echo $fastq1|sed "s#.fastq\|.fq\|.fastq.gz\|.fq.gz##g").$(echo $header | head -n 1 | grep -Eo "[ATGCN]+$")"
cat> $outputs/$fastq1.fq2ubam.json<<EOF
{
"ConvertPairedFastQsToUnmappedBamWf.readgroup_name": "${ID}.${SM}",
  "ConvertPairedFastQsToUnmappedBamWf.sample_name": "${SM}",
  "ConvertPairedFastQsToUnmappedBamWf.fastq_1": "$1",
  "ConvertPairedFastQsToUnmappedBamWf.fastq_2": "$fastq2",
  "ConvertPairedFastQsToUnmappedBamWf.library_name": "${LB}",
  "ConvertPairedFastQsToUnmappedBamWf.platform_unit": "${PU}.${SM}",
  "ConvertPairedFastQsToUnmappedBamWf.run_date": "2016-09-01T02:00:00+0200",
  "ConvertPairedFastQsToUnmappedBamWf.platform_name": "ILLUMINA",
  "ConvertPairedFastQsToUnmappedBamWf.sequencing_center": "BI",

  "ConvertPairedFastQsToUnmappedBamWf.make_fofn": "true"
  }
EOF