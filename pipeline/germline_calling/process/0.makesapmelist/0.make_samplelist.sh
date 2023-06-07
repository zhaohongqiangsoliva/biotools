
ls *f*q.gz | parallel --max-args=2 echo |sed "s# #,#g"| awk -F'[_,]' '{print 1","$1",L"NR","$0}'>sample.csv

cat sample.csv |awk -F',' -v name=$(pwd)  'BEGIN {  print "patient,sample,lane,fastq1,fastq2"  } {print $1","$2","$3","name"/"$(NF-1)","name"/"$NF}'|less>samplelist.csv
