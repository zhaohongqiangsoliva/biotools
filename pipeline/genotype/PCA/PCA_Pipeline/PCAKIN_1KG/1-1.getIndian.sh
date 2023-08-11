# Split by chr

pp -j 1 -q wecho "
    plink
        --bfile ../data/merged
        --chr {}
        --make-bed
        --out data/indian.chr{}
" :::: chr.sh
