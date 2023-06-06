# PCA and kinship estimation for plink format input.
# - INPUT file already passed QC and LD prunning.
# 487410 individuals, 197891 variants, 4 hours for PCA.


inf="data/pruned.qc.all.chr"
dir="results"
outbase="results/pca"
wecho "
    flashpca_x86-64 --bfile $inf
        # threads 5, top 10 pcs.
        -n 5 -d 10
        --outpc ${outbase}.pc
        --outpve ${outbase}.pc.variance
    &&
        gzip -f ${outbase}.pc*
    &&
        rm -f eigenvalues.txt eigenvectors.txt
    # kinship estimation by plink2.
    # it's not necessary to do LD-pruning for kinship estimation.
    # http://people.virginia.edu/~wc9c/KING/manual.html
    &&
    plink2 --bfile $inf
        --allow-no-sex
        --memory 30000m
        --make-king-table
        --maf 0.01
        # Only report 3rd degree or closer.
        --king-table-filter 0.04
        --out $dir/kinship
    &&
        cat $dir/kinship.kin0
        | awk '\$8>=0.045'
        | body sort -k8,8gr
        | gzip >$dir/sorted.kin.3rd.gz
    &&
        rm -f $dir/kinship.kin0
"
