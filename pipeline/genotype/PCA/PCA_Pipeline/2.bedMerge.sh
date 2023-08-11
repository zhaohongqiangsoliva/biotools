#!/usr/bin/env bash 



function bedmerge()
{
prefix_1=$1
prefix_2=$2
if [ ! -n "$3" ];then
  thread=$3
else
  # shellcheck disable=SC2034
  thread=22
fi
(parallel -j 1 -q wecho "
   sh bin/PCAKIN_1KG/mergeBedPlink.sh
        result/merge/merged.chr{}
        rawdata/bed_${prefix_1}/${prefix_1}_chr{}
        rawdata/bed_shanghai_final_passFilter/${prefix_2}_{}
        {}
    | bash
" :::: chr.sh)|parallel -j 22

rm *temp*
}

bedmerge $1 $2