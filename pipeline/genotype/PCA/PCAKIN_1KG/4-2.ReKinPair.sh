# Clean kinship pair.

wecho "
    zcat data/sorted.kin.3rd.gz
    | tail -n +2
    | wcut -f1,3,8
    | awk '{if(\$3>=0.0442) print \$0;}' | mycut -f2,1 | python3 $PPATH/ClearPair.py
    |gzip >data/removed.kin.gz
"
