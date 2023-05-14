# make site level QC.
pp -j 1 -q wecho "
    plink --bfile data/merged.chr{}
        --geno 0.05
        --maf 0.001
        --hwe 1e-10
        --make-bed
        --out data/qc.chr{}
" :::: chr.sh
