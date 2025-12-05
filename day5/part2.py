def count_unique_numbers(range_file):
    
    ranges = []
        
    with open(range_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and '-' in line:
                try:
                    start_str, end_str = line.split('-', 1)
                    start = int(start_str.strip())
                    end = int(end_str.strip())
                    
                    if start > end:
                        start, end = end, start
                    
                    ranges.append((start, end))
                except ValueError:
                    continue
    
    if not ranges:
        return 0
        
    ranges.sort()    
    
    merged = []
    total_count = 0
    
    for start, end in ranges:
        if not merged:
            merged.append([start, end])
            total_count += (end - start + 1)
        else:
            last_start, last_end = merged[-1]
            
            if start <= last_end + 1:  
                if end > last_end:                    
                    total_count += (end - last_end)
                    merged[-1][1] = end
            else:                
                merged.append([start, end])
                total_count += (end - start + 1)
    
    return total_count

if __name__ == "__main__":
    
    count2 = count_unique_numbers("input-range.txt")
    print(f"Result: {count2}")
        