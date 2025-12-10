from collections import deque

def read_data(filename):
    
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
    
    targets = []
    buttons_list = []
    
    for line in lines:
        if not line.strip():
            continue
        
        # Extract target pattern
        if '[' in line and ']' in line:
            start = line.find('[') + 1
            end = line.find(']')
            target = line[start:end]
            targets.append(target)
        
        # Extract all button groups
        buttons = []
        temp_line = line[end+1:] if ']' in line else line
        
        while '(' in temp_line and ')' in temp_line:
            start = temp_line.find('(') + 1
            end = temp_line.find(')')
            indices_str = temp_line[start:end]
            
            if ',' in indices_str:
                indices = [int(idx.strip()) for idx in indices_str.split(',')]
            else:
                indices = [int(indices_str.strip())] if indices_str.strip() else []
            
            buttons.append(indices)
            temp_line = temp_line[end+1:]
        
        buttons_list.append(buttons)
    
    return targets, buttons_list


def solve_bfs(target, buttons):
    
    n = len(target)
    
    # Convert target to tuple of 0s and 1s
    target_state = tuple(1 if c == '#' else 0 for c in target)
    
    # Start state: all lights off (0)
    start_state = tuple(0 for _ in range(n))
    
    if start_state == target_state:
        return 0
    
    queue = deque([(start_state, 0)])
    visited = {start_state}
    
    while queue:
        state, presses = queue.popleft()
        
        # Try pressing each button
        for button in buttons:
            new_state = list(state)
            for idx in button:
                if 0 <= idx < n:
                    # Toggle light at index idx
                    new_state[idx] = 1 - new_state[idx]
            
            new_state_tuple = tuple(new_state)
            
            if new_state_tuple == target_state:
                return presses + 1
            
            if new_state_tuple not in visited:
                visited.add(new_state_tuple)
                queue.append((new_state_tuple, presses + 1))
    
    return float('inf')


def main():
       
    # Read data
    targets, buttons_list = read_data('input.txt')
        
    total_presses = 0
    results = []
    
    for i, (target, buttons) in enumerate(zip(targets, buttons_list)):
        min_presses = solve_bfs(target, buttons)
        
        print(f"Row {i+1}:Target: [{target}] Number of buttons: {len(buttons)}  Minimum presses: {min_presses}")        
        
        total_presses += min_presses
        results.append(min_presses)
    
    print("_" * 100)
    print(f"Row results: {results}")
    print(f"TOTAL MINIMUM PRESSES: {total_presses}")
    
    return total_presses

if __name__ == "__main__":    
    result = main()