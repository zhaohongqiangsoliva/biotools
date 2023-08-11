# Merge different chr together for pruned data,

wecho "
    printf 'data/qc.chr%s\n' {1..22} >temp.txt
    &&
    plink --merge-list temp.txt
    --make-bed
    //IMPORTANT, keey the order as the input.
    //--indiv-sort file data/clean.chr1.fam
    --out data/qc.all.chr
    &&
    rm temp.txt
"
