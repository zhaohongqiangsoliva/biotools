use bio::io::fasta::IndexedReader;
use docopt::Docopt;
use std::fs::File;
use std::io::{self, Read};
use std::process;

const USAGE: &str = "
Usage:
  fasta_reader -R <fasta> -I <fasta_fai> [-f <title_or_index>]

Options:
  -R, --fasta <fasta>             Path to FASTA file
  -I, --fasta_fai <fasta_fai>     Path to FASTA index (.fai) file
  -f, --find <title_or_index>     Title string or index to find
";

#[derive(Debug, Deserialize)]
struct Args {
    flag_fasta: String,
    flag_fasta_fai: String,
    flag_find: Option<String>,
}

fn main() -> io::Result<()> {
    let args: Args = Docopt::new(USAGE)
        .and_then(|d| d.deserialize())
        .unwrap_or_else(|e| e.exit());

    // 打开 FASTA 文件和 FAI 文件
    let fasta_file = File::open(&args.flag_fasta)?;
    let fai_file = File::open(&args.flag_fasta_fai)?;

    // 创建 IndexedReader 对象
    let reader = IndexedReader::new(fasta_file, fai_file).unwrap();

    let mut input = String::new();
    io::stdin().read_to_string(&mut input)?;

    let mut lines = input.lines();
    while let Some(line) = lines.next() {
        let parts: Vec<&str> = line.trim().split_whitespace().collect();
        if parts.len() >= 3 {
            let target_sequence_name = parts[0];
            let target_start = parts[1].parse::<usize>().unwrap_or(1);
            let target_stop = parts[2].parse::<usize>().unwrap_or(target_start);

            if let Some(find_string) = &args.flag_find {
                if target_sequence_name.contains(find_string) {
                    fetch_and_print_sequence(&reader, target_sequence_name, target_start, target_stop);
                }
            } else {
                fetch_and_print_sequence(&reader, target_sequence_name, target_start, target_stop);
            }
        }
    }

    Ok(())
}

fn fetch_and_print_sequence(
    reader: &IndexedReader<File>,
    target_sequence_name: &str,
    target_start: usize,
    target_stop: usize,
) {
    if let Ok(mut faidx) = reader.fetch(target_sequence_name, target_start, target_stop) {
        let mut seq = Vec::new();
        if let Err(err) = faidx.read(&mut seq) {
            eprintln!("Error reading interval: {:?}", err);
            process::exit(1);
        }

        if let Ok(sequence_str) = std::str::from_utf8(&seq) {
            println!(
                "{}:{}-{}: {}",
                target_sequence_name,
                target_start,
                target_stop,
                sequence_str
            );
        } else {
            eprintln!("Failed to convert sequence to UTF-8");
            process::exit(1);
        }
    } else {
        eprintln!("Couldn't fetch interval for {}:{}", target_sequence_name, target_start);
        process::exit(1);
    }
}
