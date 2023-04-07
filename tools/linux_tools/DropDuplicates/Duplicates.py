"""temp CLI

Usage:
  code.py <file> -c <col> [-s=<sep>] [-o <output>]
  code.py -c <col> [-s=<sep>]  [-o <output>]

Options:
  -h --help     Show this screen.
  -v --version     Show version.
  -o --output       output file
  -c --col          input columns by ""
  -s --sep=STR          sep for file [default:  \t ]
"""
import sys, os
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
import pandas as pd
signal(SIGPIPE, SIG_DFL)
arg = docopt(__doc__, version='template code 1.0')

def drop_dup(df,cols):
    cols_l = [ i for i  in  cols]
    df = df.drop_duplicates(cols_l)
    return df

if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='Hsub parser')
    # parser.add_argument('input', help='input file 可以使用管道,也可以使用使用 Hsub input_file' ,nargs='?')
    # args = parser.parse_args()
    #
    print(arg)
    if arg["<file>"] is not  None:
        input_file = arg["<file>"]
    else:
        input_file  = '/dev/stdin'

    if arg["--output"]:
        output=arg['<output>']
    else:
        output=sys.stdout
    print(input_file)

    print(r"{}".format(arg['--sep']))
    pd.read_csv(input_file,sep=arg['--sep']).to_csv(output,sep=arg['--sep'])





sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()