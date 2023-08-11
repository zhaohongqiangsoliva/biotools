#!/usr/bin/env bash

mkdir -p log/{rsync,submit_cromwell,custumerRsyncQueue}
nohup python -u custumerRsyncSingleQueue.py > log/custumerRsyncQueue/running.log &
echo $! >>log/PID.list
nohup python -u rsync.py > log/rsync/running.log &
echo $! >>log/PID.list
nohup python -u submit_cromwell.py >log/submit_cromwell/running.log &
echo $! >>log/PID.list