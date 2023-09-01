#!/usr/bin/env python3

"""

    Get reference seq for position.
    @Author: wavefancy@gmail.com

    Usage:
        getRefSeq.py -f posFile -r refSeq
        getRefSeq.py -h | --help | -v | --version

    Notes:
        1. Output result to stdout.
        2. If more than two columns in 'posFile', the first two should be 'contig' and 'position',
           other columns will be directly copyed to output, and apped one column for Reference seq.

    Options:
        -f posFile          Two columns. col1: contig name(chromosome name), col2: position.
                            chr1 12345
                            chr2 12345
        -r refSeq           Fasta file for reference seq.
        -h --help           Show this screen.
        -v --version        Show version.
"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')

    refSeq = args['-r']
    pF = args['-f']  # position file.

    # print(args)
    # sys.exit(-1)

    from pyfaidx import Fasta
    # genes=Fasta(refSeq)
    genes = Fasta(refSeq, rebuild=False)

    with open(pF, 'r') as posFile:
        for line in posFile:
            line = line.strip()
            if line:
                ss = line.split()
                pos_start = int(ss[1])
                #pos_end = pos_start-1 + len(ss[2])

                try:
                    # add pos_end is match all of REF allele
                    aa = genes[ss[0]][pos_start-1: pos_start]
                except ValueError:
                    sys.stderr.write('WARNNING: In contig[%s], can not find pos: %s. SKIP: %s\n' % (
                        ss[0], ss[1], line))
                    continue
                except KeyError:
                    sys.stderr.write(
                        'WARNNING: Can not find contig: %s. SKIP: %s\n' % (ss[0], line))
                    continue

                ss.append(str(aa))
                sys.stdout.write('%s\n' % ('\t'.join(ss)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
