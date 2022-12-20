#!/bin/bash
output=$1
if [ ! -n "$2" ] ;then
    echo "you have not input a word!"
else
    sh /work/share/ac7m4df1o5/bin/cromwell/5_process/Exome_Germline_Single_Sample/gvcfcombin.sh $output
fi





sh /work/share/ac7m4df1o5/bin/cromwell/5_process/Exome_Germline_Single_Sample/run_jointcalling.sh $output
sh /work/share/ac7m4df1o5/bin/cromwell/5_process/Exome_Germline_Single_Sample/run_hard_filter.sh $output