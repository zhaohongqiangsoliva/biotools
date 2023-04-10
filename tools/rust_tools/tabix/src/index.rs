use std::fs::File;
use std::io::{BufReader, BufWriter};
use flate2::write::GzEncoder;
use flate2::Compression;

fn compress_file(input_file: &str, output_file: &str) -> std::io::Result<()> {
    let input = File::open(input_file)?;
    let reader = BufReader::new(input);
    let output = File::create(output_file)?;
    let writer = BufWriter::new(output);
    let mut encoder = GzEncoder::new(writer, Compression::default());
    for line in reader.lines() {
        let line = line?;
        encoder.write_all(line.as_bytes())?;
        encoder.write_all(b"\n")?;
    }
    encoder.finish()?;
    Ok(())
}
