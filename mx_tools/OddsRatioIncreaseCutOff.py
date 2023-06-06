#!/usr/bin/env python3

"""

    Estimate the OR based on a specific cutoff. Every value will be checked as a cutoff.

    @Author: wavefancy@gmail.com

    Usage:
        OddsRatioIncreaseCutOff.py
        OddsRatioIncreaseCutOff.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data from stdin, and output to stdout.
            - Two columns, (binary_label, value) sorted by value.
            - Output will be sorted by value.
        2. See example by -f.

    Options:
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.
"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

def ShowFormat():
    '''Input File format example:'''
    print('''
#input:
------------------------
0       5
1       4
0       3
1       2
0       1
0       0

#output:
------------------------
0       5.0000e+00      NA
1       4.0000e+00      3.0000e+00
0       3.0000e+00      1.0000e+00
1       2.0000e+00      NA
0       1.0000e+00      NA
0       0.0000e+00      NA
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    data = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            try:
                x = int(ss[0])
                y = float(ss[1])
                data.append([x,y])
            except Exception as e:
                sys.stderr.write('Parse value error (SKIPPED): %s\n'%(line))

    data = sorted(data, key=lambda x:x[1], reverse=True)

    b_data = [x[0] for x in data]
    out = []
    for i in range(len(b_data)):
        top = b_data[0:i+1]
        bottom = b_data[i+1:]
        t_0 = top.count(0)
        t_1 = top.count(1)
        b_0 = bottom.count(0)
        b_1 = bottom.count(1)

        if t_0 * t_1 * b_0 * b_1 == 0:
            out.append('NA')
        else:
            out.append('%.4e'%((t_1*1.0/t_0)/(b_1*1.0/b_0)))

    #output results.
    for x,y in zip(data,out):
        sys.stdout.write('%d\t%.4e\t%s\n'%(x[0],x[1],y))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
