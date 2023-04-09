hrun "
cat $1
|python bin/VCF_filter/VCFDPFilter.py --mindp 5
|python bin/VCF_filter/VCFGQFilter.py --mingq 20
#|python bin/VCF_filter/VCFHETMinorReadsRatioFilter.py -c 0.2
#|python bin/VCF_filter/VCFHOMOMinorReadsRatioFilter.py -c 0.1
#|python bin/VCF_filter/VCFSiteMissingFilter.py -m 0.3
#|python bin/VCF_filter/VCFreFORMATGeno.py -t GT
#|python bin/VCF_filter/VCFSetID.py
|bgzip > $2
"
