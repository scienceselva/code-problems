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

def step(g):

    changed = False
    replaced_count = 0
    new_g = [row[:] for row in g]

    for r in range(rows):
        for c in range(cols):
            if g[r][c] == '1':
                
                n1 = 0
                for dr, dc in dirs:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        if g[nr][nc] == '1':
                            n1 += 1

                if n1 < 4:
                    new_g[r][c] = '0'
                    changed = True
                    replaced_count += 1

    return new_g, changed, replaced_count

total_replaced = 0

while True:
    grid, changed, replaced_now = step(grid)
    total_replaced += replaced_now
    if not changed:
        break

result = ["".join(row) for row in grid]
for row in result:
    print(row)

print("Total 1s replaced by 0s =", total_replaced)
