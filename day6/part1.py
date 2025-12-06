def solve_worksheet(filename="input.txt"):    

        with open(filename, 'r') as f:
            lines = f.readlines()
                
        lines = [line.rstrip('\n') for line in lines]
        
        op_line_index = -1
        for i, line in enumerate(lines):
            if '+' in line or '*' in line:
                op_line_index = i
                break
        
        if op_line_index == -1:
            print("Error: No operation line found!")
            return [], 0
        
        op_line = lines[op_line_index]
        
        number_lines = [lines[i] for i in range(len(lines)) if i != op_line_index]
        

        problems = []
        current_op = ''
        
        i = 0
        while i < len(op_line):
            
            while i < len(op_line) and op_line[i] == ' ':
                i += 1
            
            #  start a new problem
            if i < len(op_line) and op_line[i] in ('+', '*'):
                current_op = op_line[i]
                problems.append({'op': current_op, 'nums': []})
                i += 1
            else:
                i += 1
        
        # Parse numbers for each problem
        for line in number_lines:
            numbers = []
            current_num = ''
                        
            for char in line:
                if char.isdigit():
                    current_num += char
                elif current_num:
                    numbers.append(int(current_num))
                    current_num = ''
                        
            if current_num:
                numbers.append(int(current_num))
                        
            for i, num in enumerate(numbers):
                if i < len(problems):
                    problems[i]['nums'].append(num)
        
        # Calculate results
        results = []
        for problem in problems:
            if problem['op'] == '+':
                result = sum(problem['nums'])
            else:  # '*'
                result = 1
                for num in problem['nums']:
                    result *= num
            results.append(result)
        
        grand_total = sum(results)
        
        return results, grand_total

if __name__ == "__main__":

    results, total = solve_worksheet()
    
    if results:
        print("\nResults:")
        for i, result in enumerate(results, 1):
            print(f"  Column {i}: {result}")
        
        print(f"\nGrand Total: {total}")
        