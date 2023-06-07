#!/bin/bash

:<<!
参数说明：
$0      脚本文件名
$1      待拆分文件名
$2      拆分后的文件的行数
$3      拆分后的文件的前缀
!

cat $1 | parallel --header : --pipe -N$2 'cat >file_{#}.csv'

