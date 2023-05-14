#!/usr/bin/env python3

'''
    ColumnSelector

    @Author: wavefancy@gmail.com
    @Version: 1.0

    @Algorithms
    1. Select or remove lines according to the values of specified column.

    @Version 2.0
    1. Add function to copy comments line, comments started by #.

    @Version 3.0
    1. Add function to read keys from file.
'''
import sys
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) #prevent IOError: [Errno 32] Broken pipe. If pipe closed by 'head'.

def help():
    sys.stderr.write('''
    -------------------------------------
    ColumnSelector
    -------------------------------------

    @Author: wavefancy@gmail.com
    @Version: 3.0

    @Usages:
    para1: Column index to compare with keys.
    para2: k|r, keep or remove those lines which indicated by keys.
    para3-n: keys. (the logic between them is OR)
    para[-f keyfile, optional]: read keys from 'keyfile'.

    @Optional:
    -c : Directly copy comment line to stdout, no action performed, comments started by #.

    @Notes:
    1. Read input from stdin, and output to stdout.
    2. Case sensitive for keys. The column value equals one of the keys will return true.
    4. Column index starts from 1.
    -------------------------------------
    \n''')
    sys.stderr.close()
    sys.exit(-1)

if __name__ == '__main__':
    args = []
    copyComments = False
    keyFile = ''
    i = 0
    while i < len(sys.argv): # parse parameters.
        if sys.argv[i] == '-c':
            copyComments = True
        elif sys.argv[i] == '-f':
            i += 1
            keyFile = sys.argv[i]
        else:
            args.append(sys.argv[i])
        i += 1

    sys.argv = args
    if len(sys.argv) < 2:
        help()

    col_index = int(sys.argv[1]) -1
    action = True # True keep, false remove.
    if sys.argv[2] == 'r':
        action = False

    #read key sets.
    keys = set()
    if keyFile:
        with open(keyFile, 'r') as kFile:
            for line in kFile:
                line = line.strip()
                if line:
                    keys.add(line)
        #read keys from arguments.
        keys = keys.union(set(sys.argv[2:]))
    else:
        keys = set(sys.argv[3:])

    for line in sys.stdin:
        line = line.strip()
        if line :
            if copyComments and line.startswith('#'):
                sys.stdout.write('%s\n'%(line))
                continue

            ss = line.split(None,col_index+1)

            if action: #keep
                if ss[col_index] in keys:
                    sys.stdout.write('%s\n'%(line))
            else:
                if ss[col_index] not in keys:
                    sys.stdout.write('%s\n'%(line))


sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
