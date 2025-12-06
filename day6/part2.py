with open('input.txt') as f:
    lines = [line.rstrip('\n') for line in f]

maxlen = int(len(lines[4]))
maxrows = 5
operators = {"+", "*"}
current_operator = None
main_result = 0
row_result = 0

print(f"Maxlen: {maxlen}")
print(f"Maxrows: {maxrows}")

for i in range(maxlen):

    operatorchange_flag = False    
    current_number = ""
    for j in range(maxrows):

        ch = lines[j][i]
        #print(f"Ch{i}{j}: {ch}")
        if ch.isdigit():
            current_number = current_number + ch
        else:        
            if ch in operators:
                current_operator = ch
                operatorchange_flag = True
            elif ch.isspace():
                pass  
            else:
                print(f"Invalid character {ch} at index {i}")

    if current_number.strip():
        new_number = int(current_number)
    else:
        new_number = 0   # safe default
    
    if operatorchange_flag:
        main_result += int(row_result)
        print(f"=========> row Result: {row_result}")
        row_result = 0

    if current_operator == "+":
        row_result += int(new_number)
    elif current_operator == "*":
        if row_result == 0:
            row_result = 1
        if new_number == 0:
            new_number = 1
        row_result *= int(new_number)
    #print(f"operator: {current_operator} :rowres: {new_number} :rowres: {row_result}")

main_result += int(row_result)
print(f"Result: {main_result}")
