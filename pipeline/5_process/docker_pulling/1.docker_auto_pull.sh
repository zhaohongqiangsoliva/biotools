#!/bin/bash
# input dockerlist file
cat $1 | while read line
do
  echo "docker images name is :${line}"
  docker pull ${line}
  sub_name=${line//// };
  name=($sub_name)
  len=${#name[@]}
  echo "length $len"
  pkg=`echo ${name[$len-1]}".tar"|sed "s#:#_#g"`
  echo "docker save $line -o $pkg"
  docker save $line -o $pkg
done
