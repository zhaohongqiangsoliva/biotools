#!/usr/bin/env python

"""

    Extract pattern by python regular expression.
    @Author: wavefancy@gmail.com

    Usage:
        GetPatternList.py -p rePattern [-a]
        GetPatternList.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data from stdin, and output results to stdout.
        2. Applay function: re.findall(pattern, string),
            string either from all the data from stdin,
                   or line by line.
        3. See example by -f.

    Options:
        -p rePattern  Python regular pattern.
        -a            Read all data then apply search function, defualt line by line.
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
    #Input data.
    ------------------------
x12=34
x34=56
s12=x45

    #output:
    ------------------------
x12=
x34=

    #Greedy and non-greedy search:
    ------------------------
#*?, +?, ??
#The '*', '+', and '?' qualifiers are all greedy; they match as much text as possible. Sometimes this behaviour isn’t desired; i
f the RE <.*> is matched against '<H1>title</H1>', it will match the entire string, and not just '<H1>'. Adding '?' after the qu
alifier makes it perform the match in non-greedy or minimal fashion; as few characters as possible will be matched. Using .*? in
 the previous expression will match only '<H1>'.

    ''');

class P(object):
    pattern = ''

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    P.pattern = args['-p']

    import re
    if args['-a']:
        ss = ''
        for line in sys.stdin:
            ss += line

        out = re.findall(P.pattern, ss)
        sys.stdout.write('%s\n'%('\n'.join(out)))

    else:
        for line in sys.stdin:
            line = line.strip()
            if line:
                out = re.findall(P.pattern, line)
                if out:
                    sys.stdout.write('%s\n'%('\n'.join(out)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
