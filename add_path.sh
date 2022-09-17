#!/bin/bash
SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)
if [ ! -d "${SHELL_FOLDER}/../bin" ]; then
  SHELL_FOLDER_bin=$(cd "$(dirname "$0")";pwd)/bin
   
else
    SHELL_FOLDER_bin=$(cd "$(dirname "$0")";pwd)/../bin
fi

read -r -p "${SHELL_FOLDER_bin} Do u wanna adding it to PATH? [Y/n] " input
 
case $input in
    [yY][eE][sS]|[yY])
        for i in `find ${SHELL_FOLDER} -name "*sh" -o -name "*py"`
        do
            ln -sf $i ${SHELL_FOLDER_bin}
        done
        echo export PATH="$PATH:${SHELL_FOLDER_bin}">>~/.bashrc
        echo export PATH="$PATH:${SHELL_FOLDER_bin}">>~/.zshrc
        
        ;;
 
    [nN][oO]|[nN])
        exit 1
           ;;
 
    *)
        echo "Invalid input..."
        exit 1
        ;;
esac
