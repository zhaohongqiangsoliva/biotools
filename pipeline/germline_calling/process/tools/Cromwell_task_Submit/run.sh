## submit task as cromwell server
#make a sample csv
# easy to make way
  # ls `pwd`/*f*q.gz | parallel --max-args=2 echo |sed "s# #,#g"|awk ' BEGIN {  print "patient,sample,lane,fastq1,fastq2"  } {print "1,WYH220816,""L"NR","$0}'
  #
  #ls *f*q.gz | parallel --max-args=2 echo |sed "s# #,#g"| awk -F'[_,]' '{print NR","$1",L"NR","$0}'>sample.csv
  #
  #cat sample.csv |awk -F',' -v name=$(pwd)  'BEGIN {  print "patient,sample,lane,fastq1,fastq2"  } {print $1","$2","$3","name"/"$(NF-1)","name"/"$NF}'|less>samplelist.csv


cat sample.csv|cromwell_task_submit.py -p <pipe> -b <bed file(only wes need)>