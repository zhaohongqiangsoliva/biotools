#!/usr/bin/env python

'''
    RemoveDuplicateTitle

    @Author: wavefancy@gmail.com, Wallace Wang
    @Version: 1.0

    @Algorithms:
    1. Copy the first line as title, remove all the other lines
        if they have the same content as the title line.

'''
import sys
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) #prevent IOError: [Errno 32] Broken pipe. If pipe closed by 'head'.

def help():
    sys.stderr.write('''
    -------------------------------------
    RemoveDuplicateTitle
    -------------------------------------

    @Author: wavefancy@gmail.com
    @Version: 1.0

    @Notes:
    1. Read from stdin and output to stdout.
    2. Copy the first line as title line, remove all the other lines
        IF they have the same content as the title line.
    -------------------------------------
    \n''')
    sys.stderr.close()
    sys.exit(-1)

if __name__ == '__main__':
    if(len(sys.argv) != 1):
        help()

    title = ''
    firstLine = False
    for line in sys.stdin:
        if not firstLine:
            firstLine = True
            title = line
            sys.stdout.write(line)
        elif not line == title:
            sys.stdout.write(line)

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
