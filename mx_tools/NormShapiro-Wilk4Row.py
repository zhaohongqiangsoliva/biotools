#!/usr/bin/env python3

"""

    Perform the Shapiro-Wilk test for normality.

    For N > 5000 the W test statistic is accurate but the p-value may not be.
    The chance of rejecting the null hypothesis when it is true is close to 5% regardless of sample size.
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.shapiro.html

    @Author: wavefancy@gmail.com

    Usage:
        NormShapiro-Wilk4Row.py [-l]
        NormShapiro-Wilk4Row.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read content from stdin, and output selected lines to stdout.
        2. Line index start from 1.

    Options:
        -l            Indicate the first column as label.
        -h --help     Show this screen.
        -v --version  Show version.

    Dependency:
        scipy

"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

def ShowFormat():
    '''Input File format example:'''
    print('''
# input
------------------------
X1 1 2 4 4 5 6 3 2 1
X2 1 1 1 1 1 2 2 2 2

#output: -l
------------------------
NAME    W       PValue
X1      0.936162        5.4213e-01
X2      0.654736        4.1939e-04
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    FIRST_LABEL = True if args['-l'] else False
    import scipy.stats as stats

    if FIRST_LABEL:
        sys.stdout.write('NAME\tW\tPValue\n')
    else:
        sys.stdout.write('W\tPValue\n')

    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            out = []
            if FIRST_LABEL:
                out.append(ss[0])
                ss = [float(x) for x in ss[1:]]
            else:
                ss = [float(x) for x in ss]

        w,p = stats.shapiro(ss)
        out.append('%f'%(w))
        out.append('%.4e'%(p))
        sys.stdout.write('%s\n'%('\t'.join(out)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
