#!/bin/bash
grep -v "^#" $1 | \
    cut -f 8 | \
    sed 's/^.*;DP=\([0-9]*\);.*$/\1/' |datamash mean 1 sstdev 1| awk '{print $1+3*$2}'