import sys, os
import argparse
from signal import signal, SIGPIPE, SIG_DFL

signal(SIGPIPE, SIG_DFL)


def rsync_cmd(rsa_file, port, path1, path2):
    if rsa_file:
        os.system(
            f"""rsync -avrP  -e "ssh -p {port} -i {rsa_file}" {path1} {path2} && touch download_done""")
    else:
        os.system(
            f"""rsync -avrP  -e "ssh -p {port} " {path1} {path2} && touch download_done""")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hsub parser')
    parser.add_argument('up', help='上传', nargs='?')
    parser.add_argument('download', help='下载', nargs='?')
    parser.add_argument("-n", default="zhaohq")
    parser.add_argument("-ip", default="ip addr")
    parser.add_argument("-rsa", help="rsa file path")
    parser.add_argument("-p",default="22")
    args = parser.parse_args()

    locals_path = sys.argv[-2]
    remote_path = sys.argv[-1]
    name_ip = args.n + ":" + args.ip
    rsa_file = args.rsa
    remote = f"""{name_ip}:{remote_path}"""
    port = args.p
    if args.up:
        rsync_cmd(rsa_file, port, locals_path, remote)
    elif args.download:
        rsync_cmd(rsa_file, port,  remote, locals_path)

    else:
        print("please input up or down")
        exit(1)
sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
