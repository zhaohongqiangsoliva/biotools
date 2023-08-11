"""Usage: cut.py [-d DELIMITER] (-f KEYS | FIELD ...) [-m]

Cut fields from input (file or stdin) and print them to stdout.

Arguments:
  FIELD                  Field indices to cut (1-based).

Options:
  -d DELIMITER, --delimiter DELIMITER   Field delimiter [default: ,].
  -f KEYS, --keys KEYS   Comma-separated field keys to cut (e.g., "key1,key2").
  -m, --ignore-comments  Ignore lines starting with '#' character.
  -h, --help                            Show this help message and exit.

Examples:
  1. Read from file using field indices:
     python cut.py -d , 1 3 4 <input_file.txt

  2. Read from stdin using field indices:
     cat input_file.txt | python cut.py -d , 1 3 4

  3. Read from file using field keys:
     python cut.py -d , -f "name,age" <input_file.txt

  4. Read from stdin using field keys:
     cat input_file.txt | python cut.py -d , -f "name,age"
"""

import sys
import signal
import docopt
signal.signal(signal.SIGPIPE, signal.SIG_DFL)

def cut_fields(input_stream, delimiter, fields, ignore_comments_prefix):
    for line in input_stream:
        if ignore_comments_prefix and line.startswith(ignore_comments_prefix):
            print(line, end='')  # Print the whole line (including newline) for comments
        else:
            parts = line.strip().split(delimiter)
            selected_fields = [parts[field - 1] for field in fields]
            print(delimiter.join(selected_fields))

def field_keys_to_indices(header, field_keys):
    keys = header.strip().split(',')
    return [keys.index(key) + 1 for key in field_keys]

if __name__ == "__main__":
    args = docopt.docopt(__doc__)

    delimiter = args['--delimiter']
    if args['--keys']:
        field_keys = args['--keys'].split(',')
    else:
        field_keys = None

    if args['FIELD'] and field_keys:
        print("Error: You cannot mix field indices and field keys.")
        sys.exit(1)

    ignore_comments_prefix = args['--ignore-comments']

    if sys.stdin.isatty():  # Check if stdin has data
        if len(sys.argv) < 2:
            print("Usage: python cut.py [-d DELIMITER] (-f KEYS | FIELD ...) [--ignore-comments PREFIX]")
            sys.exit(1)
        input_file = sys.argv[1]
        with open(input_file, 'r') as f:
            if ignore_comments_prefix:
                for line in f:
                    if line.startswith(ignore_comments_prefix):
                        print(line, end='')
            if field_keys:
                header = f.readline()
                fields = field_keys_to_indices(header, field_keys)
                cut_fields(f, delimiter, fields, ignore_comments_prefix)
            else:
                cut_fields(f, delimiter, [int(field) for field in args['FIELD']], ignore_comments_prefix)
    else:
        if ignore_comments_prefix:
            for line in sys.stdin:
                if line.startswith(ignore_comments_prefix):
                    print(line, end='')
        if field_keys:
            header = sys.stdin.readline()
            fields = field_keys_to_indices(header, field_keys)
            cut_fields(sys.stdin, delimiter, fields, ignore_comments_prefix)
        else:
            cut_fields(sys.stdin, delimiter, [int(field) for field in args['FIELD']], ignore_comments_prefix)

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()