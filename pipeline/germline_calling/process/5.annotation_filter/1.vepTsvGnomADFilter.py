"""temp CLI

Usage:
  code.py <file>
  code.py group send -f <file> [<delaytime>]
  code.py [INPUT ...] [options]

Options:
  -h --help     Show this screen.
  -v --version     Show version.
  -o --output       output file
  -H --header       header is true
  -c --command      save command to file
"""
import sys, os,re
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)
arguments = docopt(__doc__, version='template code 1.0')

def Pathogenic(line_list):
    max_af,gnm_af =0,0
    if line_list[col["MAX_AF"]] == ".":
        max_af = 0
    else:
        max_af = line_list[col["MAX_AF"]]
    if line_list[col["gnomAD_AF"]] == ".":
        gnm_af = 0
    else:
        gnm_af = line_list[col["gnomAD_AF"]]
    af = max(float(max_af) , float(gnm_af))

    if af < 0.01:
        #if len(re.findall('|'.join(["downstream", "intron", "synonymous", "upstream", "non_coding"]),line_list[col["Consequence"]])) == 0:
            if line_list[col["IMPACT"]]  != "MODIFIER" and line_list[col["IMPACT"]]  != "LOW":
                return True
    else:
        return False


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='Hsub parser')
    # parser.add_argument('input', help='input file 可以使用管道,也可以使用使用 Hsub input_file' ,nargs='?')
    # args = parser.parse_args()
    #
    if arguments["<file>"] is not  None:
        input_file = arguments["<file>"]
    else:
        input_file  = '/dev/stdin'

    line_num = 0
    col = {}
    for line in sys.stdin:
        line=line.strip()
        line_list = line.split()
        line_num += 1

        if line_num==1 and arguments["--header"]:
            sys.stdout.write(line+"\n")
            col=dict(map(reversed, enumerate(line_list)))
            continue
        if Pathogenic(line_list):
            sys.stdout.write(line + "\n")

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()