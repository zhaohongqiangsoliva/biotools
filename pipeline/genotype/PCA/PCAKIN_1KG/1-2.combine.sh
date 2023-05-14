# Combine UKBB data with imputed batch12 data.

pp -j 1 -q wecho "
    mergeBedPlink.sh
        data/merged.chr{}
        data/indian.chr{}
        /medpop/esp2/projects/1000G/release/20130502/ftp-trace.ncbi.nih.gov/1000genomes/ftp/release/plink_bed_multialleleic/chr{}.phase3_shapeit2_mvncall_integrated_v5a.20130502
    | bash
" :::: chr.sh
