with open('input.txt') as f:
    lines = [line.rstrip('\n') for line in f]

# ---- total number of ^ symbols
total = 0
for line in lines:
    total += line.count("^")

print(f"Total: {total}")

# --------------------------------------------------

maxrows= len(lines[0])
maxlen = len(lines)
split_count=0

newout =[]
prev_list = lines[0]

for i in range(maxlen):

    line_list = list(lines[i])
    
    for j in range(maxrows):
        ch = lines[i][j]        
        ph = prev_list[j]  
        
        if ch == "^":
            if split_count == 0:
                               
                line_list[j-1] = "|"
                line_list[j+1] = "|"
                split_count += 1

            elif ph == "|":
                                
                line_list[j-1] = "|"
                line_list[j+1] = "|"
                split_count += 1
            else:
                pass
        elif ph == "|":            
            line_list[j] = "|"
        else:
            pass
    prev_list = line_list

    newout.append(line_list)


# just a sample of output for checking the code
with open('output.txt', 'w') as file:
    for inner_list in newout:        
        line = ''.join(inner_list)
        file.write(line + '\n')


print(f"Split count: {split_count}")








