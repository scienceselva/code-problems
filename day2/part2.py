def find_invalid_ids_fast(ranges_str):    
    ranges = [r.strip() for r in ranges_str.split(',')]
    total_invalid = 0
    
    for r in ranges:
        if '-' in r:
            start, end = map(int, r.split('-'))            
            
            for num in range(start, end + 1):
                str_num = str(num)
                length = len(str_num)
                
                found = False                
                for pattern_len in range(1, length // 2 + 1):
                    if length % pattern_len != 0:
                        continue
                    
                    repetitions = length // pattern_len
                    if repetitions < 2:
                        continue
                    
                    pattern = str_num[:pattern_len]
                                        
                    if pattern != '0' and pattern[0] == '0':
                        continue                    
                   
                    if str_num == pattern * repetitions:
                        total_invalid += num
                        found = True
                        break
    
    return total_invalid

input_ranges = "959516-995437,389276443-389465477,683-1336,15687-26722,91613-136893,4-18,6736-12582,92850684-93066214,65-101,6868676926-6868700146,535033-570760,826141-957696,365650-534331,1502-2812,309789-352254,79110404-79172400,18286593-18485520,34376-65398,26-63,3333208697-3333457635,202007-307147,1859689-1936942,9959142-10053234,2318919-2420944,5142771457-5142940464,1036065-1206184,46314118-46413048,3367-6093,237-481,591751-793578"

result = find_invalid_ids_fast(input_ranges)
print(f" Final result: {result}")