#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: soliva
@Site:
@file: hrun.py
@time: 2022/11/23
@desc:
format hrun "
            command 1
            |command 2
            |command 3
"
hrun EOF
            command 1
            |command 2
            |command 3
EOF

'''
import re
import sys, os
import argparse
import datetime
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)
import subprocess as sb


def running(commands):
    '''
    running subprocess popen fun to running Command line
    '''

    process = sb.Popen(commands, stdin=sb.PIPE, stdout=sb.PIPE,shell=True,executable='/bin/bash')
    out, err = process.communicate()
    return out,err





if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hsub parser format hrun " \
            command 1 \
            |command 2 \
            |command 3 \
"')
    parser.add_argument('input', help='input file or hrun input_file' ,nargs='?')
    parser.add_argument("-s",help="save code path")
    args = parser.parse_args()

    if args.input is not  None:
        inputs = args.input
    else:
        inputs  = open('/dev/stdin').read()

    commentDelimeter = '%%'
    # linecomment = '//'
    linecomment = '#'
    linebreaker = '!!'


    lines = inputs.strip()
    lines = lines.split(commentDelimeter)
    if len(lines) % 2 == 0:
        sys.stderr.write('Error: Comment delimter should be appeared in pair!.\n')
        sys.exit(-1)

    cmd_arr = []
    for line in lines:
        for cmd in line.split("\n"):
            cmd=cmd.strip()
            if cmd.startswith(linecomment) or cmd.startswith(linebreaker)  :
                pass
            else:
                if "@(" in cmd:

                    prior = re.findall("(?<=\@\().*?(?=\))",cmd)
                    for sub_cmd in prior:
                        out,err = running(sub_cmd)
                        new = cmd.replace(f"""@({sub_cmd})""",str(out.strip(),encoding = "utf-8"))
                        cmd_arr.append(new)

                else:
                    cmd_arr.append(cmd)
    sys.stdout.write(' '.join(cmd_arr)+"\n")
    if args.s:
        with open(args.s,"w") as f:
            f.write(' '.join(cmd_arr))
sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()