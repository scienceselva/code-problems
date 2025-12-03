with open('input.txt') as f:
    lines = [line.rstrip('\n') for line in f]

def find_largest_two_digit_optimal(number_str):
    
    if len(number_str) < 2:
        return "00"
    
    n = len(number_str)
    best_value = -1
    best_pair = ""
    

    for i in range(n - 1):
        first_digit = number_str[i]
        
       
        max_after = '0'
        for j in range(i + 1, n):
            if number_str[j] > max_after:
                max_after = number_str[j]
        
       
        pair = first_digit + max_after
        value = int(pair)
        if value > best_value:
            best_value = value
            best_pair = pair
    
    return best_pair


total = 0
for line in lines:
    result = find_largest_two_digit_optimal(line)    
    print(f"{line} -> {result}")
    total += int(result)

print(f"Total: {total}")
