# PCA data with outliers from PCA and kinship removed.

wecho "
    zcat data/pop.all.pca.gz
    | SubsetByKeyV3.py data/removed.pca.kin.txt e 2
    | gzip >data/no.outliers.pop.all.pca.gz
"
