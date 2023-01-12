find `pwd` -name "*fastq*" |xargs ls -l|awk '{print $5,$NF}' > size.txt
sed -i -r "s#\/data.*\/R#R#g" size.txt