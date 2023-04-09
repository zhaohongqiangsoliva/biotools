
#查看深度
samtools depth  bamfile  |  awk '{sum+=$3} END { print "Average = "sum/NR}'


samtools depth *bamfile*  |  awk '{sum+=$3; sumsq+=$3*$3} END { print "Average = ",sum/NR; print "Stdev = ",sqrt(sumsq/NR - (sum/NR)**2)}'

#查看覆盖度
bedtools genomecov -d -ibam your_bam.bam -g your_genome.fa > genome_cov.txt


qualimap bamqc -bam you_bam_file.bam -outfile report.pdf -outformat PDF