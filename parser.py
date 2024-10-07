import re
import csv
import sys

def parse_iperf_log(file_path):
    # Updated regex pattern to capture the correct number of groups
    pattern = r'\[\s*(\d+)\]\s*([\d.]+)-([\d.]+)\s*sec\s*([\d.]+)\s*(\w+)\s*([\d.]+)\s*(\w+)/sec\s*([\d.]+)\s*ms\s*(\d+)/(\d+)\s*\(([\d.]+)%\)'
    parsed_data = []

    with open(file_path, 'r') as file:
        for line in file:
            match = re.match(pattern, line.strip())
            if match:
                id, start, end, transfer, transfer_unit, bandwidth, bandwidth_unit, jitter, lost, total, loss_percent = match.groups()
                parsed_data.append({
                    'ID': id,
                    'Interval': f"{start}-{end}",
                    'Transfer': f"{transfer} {transfer_unit}",
                    'Bandwidth': bandwidth,
                    'Jitter': jitter,
                    'Lost/Total': f"{lost}/{total}",
                    'Loss': loss_percent
                })
    
    return parsed_data

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_iperf.txt>")
        sys.exit(1)

    file_path = sys.argv[1]
    parsed_data = parse_iperf_log(file_path)

    if parsed_data:
        fieldnames = ['ID', 'Interval', 'Transfer', 'Bandwidth', 'Jitter', 'Lost/Total', 'Loss']
        
        writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
        writer.writeheader()
        for row in parsed_data:
            writer.writerow(row)
    else:
        print("Error: No valid iperf data found in the input file.")

if __name__ == "__main__":
    main()
