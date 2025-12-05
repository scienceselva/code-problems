def count_covered_ids(range_file, ids_file):
    
    with open(range_file) as f:
        ranges = []
        for line in f:
            if line.strip():
                start, end = map(int, line.strip().split('-'))
                ranges.append((start, end))
        
    with open(ids_file) as f:
        ids = [int(line.strip()) for line in f if line.strip()]
    
    # Check each ID
    covered = 0
    for id_num in ids:
        if any(start <= id_num <= end for start, end in ranges):
            covered += 1
    
    return covered

if __name__ == "__main__":
    result = count_covered_ids("input-range.txt", "input-ids.txt")
    print(f"IDs covered count: {result}")
