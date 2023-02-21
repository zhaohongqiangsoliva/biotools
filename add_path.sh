#!/bin/bash
SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)
SHELL_FOLDER_bin=$(cd "$(dirname "$0")";pwd)/bin

read -r -p "${SHELL_FOLDER_bin} Do u wanna adding it to PATH? [Y/n] " input
 
case $input in
    [yY][eE][sS]|[yY])
        echo -e "export PATH=\"\$PATH:${SHELL_FOLDER_bin}\"" >>~/.bashrc
        echo -e "export PATH=\"\$PATH:${SHELL_FOLDER_bin}\"" >>~/.zshrc
        chmod -R 777 $SHELL_FOLDER
        ;;
 
    [nN][oO]|[nN])
        exit 1
           ;;
 
    *)
        echo "Invalid input..."
        exit 1
        ;;
esac
