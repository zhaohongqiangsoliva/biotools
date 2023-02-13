
use std::env;
use std::fs::File;
use std::io::prelude::*;
use std::io::BufReader;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        panic!("Please enter the csv file path.");
    }
    let file_path = &args[1];
    let mut ordering: Vec<usize> = Vec::new();
    let mut ignore: Vec<usize> = Vec::new();
    for i in 2..args.len() {
        let arg = &args[i];
        let number = match arg.parse::<usize>() {
            Ok(num) => num,
            Err(_) => {
                if arg.starts_with("-") {
                    match arg[1..].parse::<usize>() {
                        Ok(num) => {
                            ignore.push(num);
                            continue;
                        }
                        Err(_) => {
                            println!("Invalid argument {}. Ignoring.", arg);
                            continue;
                        }
                    }
                } else {
                    println!("Invalid argument {}. Ignoring.", arg);
                    continue;
                }
            }
        };
        ordering.push(number);
    }
    let mut results: Vec<Vec<String>> = Vec::new();
    {
        let file = File::open(file_path).expect("File not found");
        let reader = BufReader::new(file);
        for line in reader.lines() {
            let line_text = line.expect("Invalid line text");
            let line_values: Vec<String> = line_text
                .split(',')
                .filter(|v| !ignore.contains(&v.parse::<usize>().unwrap_or(0)))
                .map(|v| String::from(v))
                .collect();
            let mut base_index = 0;
            let mut sub_result: Vec<String> = Vec::new();
            for i in 0..line_values.len() {
                let value = &line_values[i];
                if ordering.contains(&i) {
                    let new_index = ordering.iter().position(|x| *x == i).unwrap_or(0);
                    sub_result.insert(new_index, value.clone());
                    base_index = new_index;
                } else {
                    sub_result.insert(base_index + 1, value.clone());
                    base_index += 1;
                }
            }
            results.push(sub_result);
        }
    }
    for result in results {
        for value in result {
            print!("{},", value);
        }
        println!();
    }
}

