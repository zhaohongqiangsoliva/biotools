#!/bin/bash
# docker pull and save to tar file 
# input file is :
#us.gcr.io/broad-gotc-prod/picard-cloud:2.26.10
#us.gcr.io/broad-gatk/gatk:4.2.6.1
cat $1 | while read line
do
  echo "docker images name is :${line}"
  docker pull ${line}
  sub_name=${line//// };
  print $sub_name
  name=($sub_name)
  len=${#name[@]}
  echo "length $len"
  pkg=${name[$len-1]}".tar"
  echo "docker save $line -o $pkg"
  docker save $line -o $pkg
done
