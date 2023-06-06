#!/bin/env bash
#conda activate cromwell_env
SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)
SHELL_FOLDER_bin=$(cd "$(dirname "$0")";pwd)/bin

read -r -p "input status for cromwshell list " input
 
case $input in
    [sS])
          cromshell list -u |grep Succeeded| awk '{print "rm -rf /srv/pipeline/cromwell/cromwell-executions/"$3}'|bash
          
        ;;
 
    [fF])
        exit 1
           ;;
 
    *)
        echo "Invalid input..."
        exit 1
        ;;
esac