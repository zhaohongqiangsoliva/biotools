# Removed related pair and PCA outliers.

wecho "
cat
    <(zcat data/removed.kin.gz)
    <(zcat data/outliers.col*.gz | wcut -f2)
    | sort | uniq
    > data/removed.pca.kin.txt


"
