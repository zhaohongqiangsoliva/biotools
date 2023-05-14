"""Qingchat CLI

Usage:
  qingchat config ip <ip>
  qingchat config port <port>
  qingchat config login
  qingchat group list
  qingchat group choose <group_name>...
  qingchat group clean
  qingchat group send -t <content>
  qingchat group send -i <media>
  qingchat group send -f <file> [<delaytime>]

Options:
  -h --help     Show this screen.
  -v --version     Show version.
"""
import sys, os
import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)
arguments = docopt(__doc__, version='Qingchat 0.3.2')




if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='Hsub parser')
    # parser.add_argument('input', help='input file 可以使用管道,也可以使用使用 Hsub input_file' ,nargs='?')
    # args = parser.parse_args()
    #
    # if args.input is not  None:
    #     input_file = args.input
    # else:
    #     input_file  = '/dev/stdin'

    print(arguments)



sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()