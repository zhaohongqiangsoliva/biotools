#!/bin/env bash
conda activate cromwell_env
SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)
SHELL_FOLDER_bin=$(cd "$(dirname "$0")";pwd)/bin

read -r -p "input status for cromwshell list " input
 
case $input in
    [sS])
          cromshell list -u |grep Succeeded| awk '{print $3}'
        ;;
 
    [fF])
        exit 1
           ;;
 
    *)
        echo "Invalid input..."
        exit 1
        ;;
esac