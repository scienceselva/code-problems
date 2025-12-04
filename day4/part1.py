with open('input.txt') as f:
    lines = [line.rstrip('\n') for line in f]

data = []

for line in lines:
    line = line.replace(".", "0")
    line = line.replace("@", "1")    
    data.append(line)


grid = [list(row) for row in data]

rows = len(grid)
cols = len(grid[0])

# Directions for all 8 neighbors
dirs = [
    (-1,-1), (-1,0), (-1,1),
    (0,-1),         (0,1),
    (1,-1),  (1,0), (1,1)
]

new_grid = [row[:] for row in grid] 

for r in range(rows):
    for c in range(cols):
        if grid[r][c] == '1':

            count_ones = 0
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    if grid[nr][nc] == '1':
                        count_ones += 1

            if count_ones < 4:
                new_grid[r][c] = '2'


result = ["".join(row) for row in new_grid]

for row in result:
    print(row)

total_twos = sum(row.count('2') for row in result)
print("Total 2s =", total_twos)
