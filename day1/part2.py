with open('input.txt') as f:
    lines = [line.rstrip('\n') for line in f]

directions = [line[0] for line in lines]
values = [int(line[1:]) for line in lines]

current_value = 50
array_size = 100
zero_count = 0

clock = list(range(100))

for direction, move_value in zip(directions, values):
    start_value = current_value
    
    if direction == 'L':
        # Move left decreases the number
        for _ in range(move_value):
            current_value = (current_value - 1) % array_size
            if current_value == 0:
                zero_count += 1

    else:  # 'R'
        # Move right increases the number
        for _ in range(move_value):
            current_value = (current_value + 1) % array_size
            if current_value == 0:
                zero_count += 1


print(f"number of times zero is crossed {zero_count}.")
