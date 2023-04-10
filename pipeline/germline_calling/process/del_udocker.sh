mkdir -p empty
#ll -d --time=status *|grep 11月|awk '{print "rsync --delete-before -d empty/ "$9"/"}'>rm.log
ls -d *-*|awk '{print "rsync --delete-before -d empty/ "$1"/"}'>rm.log
head rm.log
#nohup parallel -j 10 < rm.log &