# make site level QC.
parallel -j 1 -q wecho "
    plink --bfile result/merge/merged.chr{}
        --geno 0.05
        --maf 0.001
        --hwe 1e-10
        --make-bed
        --out result/QC/QC.chr{}
" :::: chr.sh
