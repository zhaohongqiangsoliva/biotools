#!/usr/bin/env bash


find `pwd` -name "*f*q.gz"|parallel --max-args=2 echo |sed "s# #,#g"|awk ' BEGIN {  print "patient,sample,lane,fastq1,fastq2"  } {print "1,WYH220816,""L"NR","$0}' >sample.csv

ls -l |grep "^d" |awk '{print $8}'|awk 'print ""' sed  -i "s###g" sample.csv