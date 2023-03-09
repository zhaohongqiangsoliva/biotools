#!/usr/bin/env python3

"""

    Filter genotype based on sample DP(read depth) tags.

    @Author: wavefancy@gmail.com

    Usage:
        VCFDPFilter.py -n minDP
        VCFDPFilter.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read vcf file from stdin, mask genotype as miss if DP tage value < 'num'.
        3. Output results to stdout.

    Options:
        -n minDP          Minimum value for DP tag(read depth),int.
        -h --help       Show this screen.
        -v --version    Show version.
        -f --format     Show format example.
"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

def ShowFormat():
    '''Input File format example:'''
    print('''
    input vcf example(abstracted):
----------------------
GT:AD:DP:GQ:PL       0/0:11,0:11:33:0,33,484 ./.     0/0

    out vcf example: -n 9
----------------------
PL:GT:GQ        0/0:11,0:11:33:0,33,484 .       .
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    from pysam import VariantFile

    vcfMetaCols=9       #number of colummns for vcf meta information.
    tags = 'DP'
    minDP = int(args['-n'])

    def reformat(geno):
        '''mask geno type according DP value.'''
        if geno[0] == '.':
            return '.'
        else:
            ss = geno.split(':')
            try:
                DPvalue = int(ss[DPIndex])
                if DPvalue < minDP:
                    return '.'
                else:
                    return geno
            except ValueError:
                return '.'

    DPIndex = -1
    def setDPIndex(oldFormatTags):
        global DPIndex
        ss = oldFormatTags.upper().split(':')
        try:
            y = ss.index(tags)
            DPIndex = y
        except ValueError:
            sys.stderr.write('ERROR: can not find tag: "%s", from input vcf FORMAT field.\n'%(x))
            sys.exit(-1)

    infile = VariantFile('-', 'r')
    sys.stdout.write(str(infile.header))
    for line in infile:
        ss = str(line).strip().split()
        out = ss[:vcfMetaCols]
        for x in ss[vcfMetaCols:]:
            if DPIndex < 0:
                setDPIndex(ss[8])
            out.append(reformat(x))

        sys.stdout.write('%s\n'%('\t'.join(out)))

    infile.close()
sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
