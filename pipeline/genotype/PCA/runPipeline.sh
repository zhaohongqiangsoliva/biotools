#!/usr/bin/env bash
set -e

prefix_1=$1
prefix_2=$2

#data clean
echo "start PCA Pipeline"
## 1.running setID
echo "running setID"

bash 1.resetID.sh $prefix_1 

## 2.