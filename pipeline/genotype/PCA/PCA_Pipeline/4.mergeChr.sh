#!/usr/local/env bash

hrun "
    printf 'result/QC/QC.chr%s\n' {1..22} >temp.txt
    &&
    plink --merge-list temp.txt
    --make-bed
    #//IMPORTANT, keey the order as the input.
    #//--indiv-sort file data/clean.chr1.fam
    --out result/QC/qc.all.chr
    &&
    rm temp.txt
"
