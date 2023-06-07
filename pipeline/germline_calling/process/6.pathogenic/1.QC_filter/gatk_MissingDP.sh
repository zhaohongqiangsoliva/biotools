vcf=$1
outputname=$2
hrun "
zcat ${vcf}|python VCFDPFilter.py --mindp 5
|python VCFSiteMissingFilter.py -m 0.3
|bgzip >${outputname}

"