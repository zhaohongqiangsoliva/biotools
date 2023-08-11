#!/usr/bin/env bash

input_file=$1

parallel -q -j 10 hrun -s log/1."${input_file}"_resetID.sh "
          zcat ${input_file}.vcf.gz
          |VCFSetID.py -s
          |bgzip > rawdata/sedID_${input_file}/${input_file}_setID.vcf.gz

          " :::: chr.sh

