
import csv


def reorder_csv(input_file, target_file, col_order):
    # Reads csv contents
    lines = []
    with open(input_file, 'r') as csv_in:
        csv_reader = csv.reader(csv_in, delimiter='\t')
        for line in csv_reader:
            lines.append(line)

    # Re-orders columns
    out_lines = []
    first_out_row = [lines[0][pos] for pos in col_order]
    out_lines.append(first_out_row)
    for line in lines[1:]:
        out_lines.append([line[pos] for pos in col_order])

    # Writes new csv
    with open(target_file, 'w') as csv_out:
        csv_writer = csv.writer(csv_out, delimiter='\t')
        csv_writer.writerows(out_lines)


# To reorder columns 3 and 1 of in_file.tsv, writing the new version
# in out_file.tsv, you could use this call:
reorder_csv('/home/soliva/test/samplelist.tsv', '/home/soliva/test/samplelistout_file.tsv', [3, 1])

# To speed up this process, you could use a coroutine, which breaks down
# the calculation into chunks that can be processed in parallel:
from asyncio import create_task, run


async def reordering_task(input_file, output_file, col_order):
    # Reads csv contents
    lines = []
    with open(input_file, 'r') as csv_in:
        csv_reader = csv.reader(csv_in, delimiter='\t')
        for line in csv_reader:
            lines.append(line)

    # Re-orders columns
    out_lines = []
    first_out_row = [lines[0][pos] for pos in col_order]
    out_lines.append(first_out_row)
    # Start a concurrent task on every line
    tasks = []
    for line in lines[1:]:
        task = create_task(reorder_rows(lines, out_lines, line, col_order))
        tasks.append(task)

    # Wait for all re-order tasks to complete
    await asyncio.gather(*tasks)

    # Writes new csv
    with open(target_file, 'w') as csv_out:
        csv_writer = csv.writer(csv_out, delimiter='\t')
        csv_writer.writerows(out_lines)


async def reorder_rows(lines, out_lines, line, col_order):
    out_lines.append([line[pos] for pos in col_order])


# To reorder columns 3 and 1 of in_file.tsv, writing the new version
# in out_file.tsv, you could use this call:
run(reordering_task('/home/soliva/test/samplelist.tsv', '/home/soliva/test/samplelistout_file.tsv', [3, 1]))
