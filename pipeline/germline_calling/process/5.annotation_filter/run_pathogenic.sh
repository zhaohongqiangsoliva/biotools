parallel -q -j 3 hrun '
cat 12.annotation_family{}.vcf
| java -jar ExomeModelFilterV2-v2.5.1/v2.5.1/ExomeModelFilterV2.5.1.jar
ped_f{}.file -mod  dom > 12.annotation_family{}_ModelFilter.txt

&&
cat 12.annotation_family{}_bcftools.txt |
python 1.vepTsvGnomADFilter.py -H > 13.annotation_family{}_bcftools_filter_gnomad.txt

&&

python 1.annotation_find_pathogenic.py
12.annotation_family{}_ModelFilter.txt
13.annotation_family{}_bcftools_filter_gnomad.txt
-o 14.filter_reuslt.family{}.csv

' :::: chr.sh