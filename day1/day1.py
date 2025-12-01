with open('input.txt') as f:
    lines = [line.rstrip('\n') for line in f]

directions = [line[0] for line in lines]
values = [int(line[1:]) for line in lines]

current_value = 50
array_size = 100

print(f"The dial starts by pointing at {current_value}.")

password = 0

for direction, move_value in zip(directions, values):
    if direction == 'L':
        current_value = (current_value - move_value) % array_size
    else:  # 'R'
        current_value = (current_value + move_value) % array_size
    
    if current_value == 0:
        password += 1
    print(f"The dial is rotated {direction}{move_value} to point at {current_value}.")

print(f"The password is {password}.")