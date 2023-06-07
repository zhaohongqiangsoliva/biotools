#![allow(unused)]

use structopt::StructOpt;
use std::fs::File;
use std::io::{Write, BufReader, BufRead, Error};
///命令行传参 pattern and path
/// Search for a pattern in a file and display the lines that contain it.
#[derive(StructOpt)]
struct Cli {
    /// The pattern to look for
    pattern: String,
    /// The path to the file to read
    // #[structopt(parse(from_os_str))]
    path: String,
}


fn main() {

    let args = Cli::from_args();

    let input = File::open(&args.path).expect("could not read file");
    let mut content = BufReader::new(input);

    let mut line = String::new();
    for line in content.lines() {
        let line = line.unwrap();
        if line.contains(&args.pattern) {

            println!("{}", line);
        }
        }

    // }

}
//  stdin stdout 方式获取文件
// use std::io::stdin;
//
// fn main() {
//     let mut total_word_count = 0;
//
//     for line in stdin().lines() {
//         let line = line.unwrap();
//         if !line.trim().is_empty() {
//             total_word_count += line.split(' ').count();
//         }
//     }
//
//     println!("Total words from stdin: {}", total_word_count)
// }