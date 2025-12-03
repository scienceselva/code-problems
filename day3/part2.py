with open('input.txt') as f:
    lines = [line.rstrip('\n') for line in f]

def find_largest_k_digits_final(number_str, k=12):
    
    n = len(number_str)
    
    if n < k:        
        return number_str
    
    result = []
    start = 0
    
    
    for i in range(k):
        
        remaining_needed = k - i - 1       

        end_search = n - remaining_needed
                
        max_digit = '0'
        max_pos = start
                
        for pos in range(start, end_search):
            current_digit = number_str[pos]
            if current_digit > max_digit:
                max_digit = current_digit
                max_pos = pos
                
                if max_digit == '9':
                    break
                
        result.append(max_digit)        
        start = max_pos + 1

    return ''.join(result)

total = 0
for line in lines:
    result = find_largest_k_digits_final(line, 12)        
    print(f"{line} -> {result}")
    total += int(result)

print(f"Total: {total}")
