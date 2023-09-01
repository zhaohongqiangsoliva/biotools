#!/usr/bin/env bash
#Awesome Command Line Tool.
#         Author:solivehong
#         email: solivehong@gmail.com
#         time:2023817
#
# Usage: arguments_example.sh <qc> [-p] PREFIX [-o] OUTNAME [-d] MAXDEPTH [-h] ...
#        arguments_example.sh <check> [-p] PREFIX [-v] VCF [-h]...
#
# Options:
#   -h    --help
#   -v    prefix of check vcfs
#   -o    outname
#   -p    prefix
#   -d    maxdepth 


# if docopts is in PATH, not needed.
# Note: docopts.sh is also found in PATH
#PATH=..:$PATH
# auto parse the header above, See: docopt_get_help_string
source docopts.sh --auto -G "$@"


# please add toosmarket hrun to ur PATH 
#at default the plink plink2 
##git clone https://github.com/docopt/docopts.git
#cd docopts
#./get_docopts.sh

#### check vcfs 
#bcftools query -f '%CHROM\t%POS\t[\t%GT:%DP:%GQ:%PL]\n'|head -n 10 >checklist
for a in ${!ARGS[@]} ; do
    echo "$a = ${ARGS[$a]}"
done

docopt_print_ARGS -G





#echo "$ARGS_PREFIX"
#echo "$ARGS_OUTNAME"

SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)

seq 22 > chr.sh


reference=/data/reference/update_gatk_v0/



if  [ -n "$ARGS_check" ] ;then
          echo "---------------------CHECK DUP AND VCF STATUS(AD,DP,PL)------------------------"
          sh $SHELL_FOLDER/1.preparevcfs.sh $ARGS_PREFIX $ARGS_VCF 

          echo "cat tmp/check/*depth.ldepth.mean|tail -n +2|datamash mean 3 sstdev 3 |bgzip > meanadd3sd.txt.gz  "
else


          echo "---------------------VCF QC--------------------------"
          #maxdepth=200
          
          sh $SHELL_FOLDER/2.QC_VCFproc.sh $ARGS_PREFIX $reference $ARGS_MAXDEPTH  |parallel -j 22 

          echo "---------------------mergevcf2pgen--------------------------"
          sh $SHELL_FOLDER/3.QC_mergevcf2pgen.sh $ARGS_OUTNAME

          echo "---------------------QC_missnes_hardy--------------------------"
          sh $SHELL_FOLDER/4.QC_missnes_hardy.sh $ARGS_OUTNAME
fi