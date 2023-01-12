
rasinfo="/data/zhaohq/wuzh02.hpccube.com_1219122313_rsa.txt"
homeinfo=zhaohq@wuzh02.hpccube.com
rsync -avrP  -e "ssh -p 65091 -i $rasinfo" $homeinfo:/work/home/zhaohq/zhaohq/project/family_calling/ ./