# Select PCA outliers.
# Estimate mean+/-sd by chip data only.

wecho "
    zcat data/pop.all.pca.gz
    | wcut -f1
    | cat -n -
    | grep CHIP
    | wcut -f1
    | gzip >temp/sel.gz
"
pp -j 1 -q wecho "
    zcat data/pop.all.pca.gz
    | wcut -f1,2,{}
    | python3 $PPATH/Outliers.py -c 3 -t 5 --sl <(zcat temp/sel.gz)
    | gzip >data/outliers.col{}.gz
" ::: 3 4 5
