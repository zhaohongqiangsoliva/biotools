#!/usr/bin/env python3

'''

    Count the number of pattern of ABBA and BABA.

    @Author: wavefancy@gmail.com, Wallace Wang.

    Usage:
        ArchaicPatternCount.py -p pattern
        ArchaicPatternCount.py -h | --help | --version | -f | --format

    Notes:
        1. Read data from stdin, and output to stdout.
            AFR, HAN, Neandertal, CHIMP

    Options:
        -p pattern    ABBA or BABA.
        -h --help     Show this screen.
        --version     Show version.
        -f --format   Show input/output file format example.

'''
import sys
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) #prevent IOError: [Errno 32] Broken pipe. If pipe closed by 'head'.
from docopt import docopt

def ShowFormat():
    '''File format example'''
    print('''
#Input file format(stdin)
------------------------
1   0   0   1
1   0   0   1
1   0   1   0
0   0   0   1
0   .   0   1
          ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)
    # sys.exit(-1)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    PATTERN = args['-p'].upper()
    if PATTERN not in ['ABBA', 'BABA']:
        sys.stderr.write('Please set proper value for -p \n')
        sys.exit(-1)

    count = 0
    for line in sys.stdin:
        line = line.strip()
        if line :
            ss = line.split()
            missing = [x for x in ss if x=='.']
            if len(missing) > 0:
                continue
            if PATTERN == 'ABBA':
                if ss[0] == ss[3] and ss[1] == ss[2]:
                    count += 1
            else: # ABAB
                if ss[0] == ss[2] and ss[1] == ss[3]:
                    count += 1

    sys.stdout.write('%d\n'%(count))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
