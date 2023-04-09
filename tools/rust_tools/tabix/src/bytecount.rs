use std::fs::{File, OpenOptions};
use std::io::{BufRead, BufReader, BufWriter, Write};
use std::path::Path;

fn calculate_metadata(input_file: &Path, index_file: &mut BufWriter<File>, block_size: usize) -> std::io::Result<()> {
    let file = File::open(input_file)?;
    let reader = BufReader::new(&file);

    let mut line_count = 0;
    let mut last_pos = 0;
    let mut last_chrom = String::new();

    for line in reader.lines() {
        let line = line?;
        let fields: Vec<_> = line.split('\t').collect();
        let chrom = fields[0];
        let pos = fields[1].parse::<u64>().unwrap();

        if chrom != last_chrom {
            // write metadata for previous block
            if line_count > 0 {
                let line = format!("{}\t{}\t{}\t{}\t{}\n", last_chrom, last_pos, pos, input_file.display(), line_count);
                index_file.write_all(line.as_bytes())?;
            }
            // start new block
            line_count = 0;
            last_pos = 0;
            last_chrom = chrom.to_string();
        }

        line_count += 1;
        if pos - last_pos > block_size as u64 {
            // write metadata for previous block
            let line = format!("{}\t{}\t{}\t{}\t{}\n", last_chrom, last_pos, pos, input_file.display(), line_count - 1);
            index_file.write_all(line.as_bytes())?;
            // start new block
            line_count = 1;
            last_pos = pos;
        }

        last_pos = pos;
    }

    // write metadata for last block
    if line_count > 0 {
        let line = format!("{}\t{}\t{}\t{}\t{}\n", last_chrom, last_pos, u64::MAX, input_file.display(), line_count);
        index_file.write_all(line.as_bytes())?;
    }

    Ok(())
}