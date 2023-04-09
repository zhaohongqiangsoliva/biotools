rust
use std::fs::File;
use std::io::{BufReader, BufWriter};

fn build_index_file(metadata_file: &str, output_file: &str) -> std::io::Result<()> {
    let metadata = File::open(metadata_file)?;
    let reader = BufReader::new(metadata);
    let output = File::create(output_file)?;
    let mut writer = BufWriter::new(output);
    let mut current_offset = 0;
    for line in reader.lines() {
        let line = line?;
        let fields: Vec<_> = line.split('\t').collect();
        let chrom = fields[0];
        let pos_start = fields[1].parse::<usize>().unwrap();
        let pos_end = fields[2].parse::<usize>().unwrap();
        let line_count = fields[3].parse::<usize>().unwrap();
        writer.write_all(chrom.as_bytes())?;
        writer.write_all(b"\t")?;
        writer.write_all(pos_start.to_string().as_bytes())?;
        writer.write_all(b"\t")?;
        writer.write_all((pos_end + 1).to_string().as_bytes())?;
        writer.write_all(b"\t")?;
        writer.write_all(current_offset.to_string().as_bytes())?;
        writer.write_all(b"\n")?;
        current_offset += line_count;
    }
    Ok(())
}