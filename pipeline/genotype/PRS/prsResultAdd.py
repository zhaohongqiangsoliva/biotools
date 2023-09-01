"""temp CLI

Usage:
  code.py [<file>]
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
import pandas as pd
import glob
import seaborn as sns
import matplotlib.pyplot as plt
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

    sscroe = glob.glob("./*.sscore")
    df = pd.read_table(sscroe[0])
    df["#IID"] = df["#IID"].str.replace("_.*", "")
    sum_df = pd.DataFrame({
        "#IID": df["#IID"],
        "effect_weight_SUM": 0
    })
    for i in sscroe:

        df = pd.read_table(i)
        df["#IID"] = df["#IID"].str.replace("0_", "")
        sum_df["effect_weight_SUM"] = df["effect_weight_SUM"] + sum_df["effect_weight_SUM"]
    sum_df.to_csv("./sumPrsscors",index=False,sep="\t")
    # sum_df.plot.kde()
    # plt.axvline(sum_df.loc[0, "effect_weight_SUM"], 0, 0.7, color="r")
    # plt.axvline(sum_df.loc[1, "effect_weight_SUM"], 0, 0.7, color="r")
    # plt.axvline(sum_df.loc[2, "effect_weight_SUM"], 0, 0.7, color="r")
    # plt.text(sum_df.loc[0, "effect_weight_SUM"], 0.20, 'hxt', rotation=0)
    # plt.text(sum_df.loc[1, "effect_weight_SUM"], 0.20, 'hxt_M', rotation=0)
    # plt.text(sum_df.loc[2, "effect_weight_SUM"], 0.20, 'hxt_F', rotation=0)
    # plt.savefig('score.pdf', dpi=800)
sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()