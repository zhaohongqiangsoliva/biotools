"""temp CLI

Usage:
  code.py <file>\
  code.py group send -f <file> [<delaytime>]
  code.py [INPUT ...] [options]

Options:
  -h --help     Show this screen.
  -v --version     Show version.
  -o --output       output file
"""
import sys, os
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)
arguments = docopt(__doc__, version='template code 1.0')




if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='Hsub parser')
    # parser.add_argument('input', help='input file 可以使用管道,也可以使用使用 Hsub input_file' ,nargs='?')
    # args = parser.parse_args()
    #
    if arguments["<file>"] is not  None:
        input_file = arguments["<file>"]
    else:
        input_file  = '/dev/stdin'
    print(input_file)
    print(arguments)



sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
