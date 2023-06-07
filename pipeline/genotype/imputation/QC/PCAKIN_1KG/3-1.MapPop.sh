# Mapping pop information for each individual.

dir="results"
wecho "
    zcat $dir/pca.pc.gz | tail -n +2
    | python3 $PPATH/KeyMapReplacer.py -k 2 -r 1
        -p <(cat /medpop/esp2/projects/1000G/release/20130502/ftp-trace.ncbi.nih.gov/1000genomes/ftp/release/20130502/integrated_call_samples_v3.20130502.ALL.panel | wcut -f1,3;
            cat ../data/b1234.all.chr.fam
                /medpop/esp/wallace/IndianPRS/batch2/set1_set2_SAS_MedGenome.fam
            | wcut -f1,6
            | ColumnReplacer.py 2 2=CHIP_CASE1,1=CHIP_CTRL,-9=WGS
            )
    | sort -k1,1r
    | WColumnSelector.py -c 1 -r -v AMR
    #map for control individual
    | gzip >$dir/pop.all.pca.gz
"
