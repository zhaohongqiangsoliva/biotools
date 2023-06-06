#!/usr/bin/env python3

"""

    Prepare data for ploting manhatton plot by CategoryPlot2.
    @Author: wavefancy@gmail.com

    Usage:
        manhattonDataHelper.py [-m string]
        manhattonDataHelper.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read results from stdin, and output results to stdout.
        2. See example by -f.

    Options:
        -m string     Mask xlabel, do not show the txticktext for these masks.
                      Eg: 17,18,21 | 21
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
#in each chromosome, pos should be sorted.
------------------------
chr1 100 10
chr1 200 5
chr1 300 2
chr2 300 5
chr2 500 15

#output:
------------------------

    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='2.2')
    # version 2.2: add the option for abline.
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    mask = args['-m'].split(',') if args['-m'] else []

    colors = ['#2678B2','#FD7F28','#339F34','#D42A2F']
    colorIndex = -1
    def getColor():
        'Rotately get the color code.'
        global colorIndex
        colorIndex += 1
        return colors[(colorIndex) % len(colors)]

    chrs = []
    xlabelPos = []
    shif = 0
    currentColor = getColor()
    lastPos = 0
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            try:
                pos = int(ss[1])
                val = float(ss[2])
                #first records
                if len(chrs) == 0:
                    chrs.append(ss[0])
                    shif = pos

                if chrs[-1] != ss[0]: #different chromosomes.
                    chrs.append(ss[0])
                    #xlabelPos.append((shif+lastPos)/2)
                    xlabelPos.append(lastPos)
                    shif = lastPos
                    currentColor = getColor()

                lastPos = pos + shif
                sys.stdout.write('%s\t%d\t%.4f\t%s\n'%(chrs[-1],lastPos, val, currentColor))
                #outPos.append(pos - shif)
                #outValues.append(val)
                #outColors.append(currentColor)

            except ValueError:
                sys.stdout.write('Can not parse value at line (skipped):%s\n'%(line))

    #post process
    #xlabelPos.append((shif+lastPos)/2)
    xlabelPos.append(lastPos)
    #print(chrs)

    #marsk some chr.
    for i in range(len(chrs)):
        if chrs[i] in mask:
            chrs[i] = 'NA'

    sys.stdout.write('COMMAND\txticktext\t%s\n'%('\t'.join(chrs)))
    sys.stdout.write('COMMAND\txtickvals\t%s\n'%('\t'.join(['%d'%(x) for x in xlabelPos])))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
