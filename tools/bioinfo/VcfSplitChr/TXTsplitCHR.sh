cut -f 1 -d " " input_file | sort | uniq | while read value; do grep "^$value" input_file > "$value.txt"; done
