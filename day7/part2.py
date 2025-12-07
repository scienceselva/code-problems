def solve_paths(filename):
    with open(filename, 'r') as f:
        grid = [line.rstrip('\n') for line in f]
    
    rows = len(grid)
    cols = len(grid[0])
    
    # Find S position  // first line 
    start_r, start_c = 0, 0
    for r in range(rows):
        if 'S' in grid[r]:
            start_r = r
            start_c = grid[r].index('S')
            break
    
    # Convert S to | for looping selva
    grid[start_r] = grid[start_r].replace('S', '|')
    
    # DP table: dp[r][c] = number of ways to reach (r, c)
    dp = [[0] * cols for _ in range(rows)]
    dp[start_r][start_c] = 1
    
    # Process each row
    for r in range(start_r, rows - 1):  # Don't process last row as source
        for c in range(cols):
            if dp[r][c] > 0 and grid[r][c] == '|':
                # Check cell directly below
                if r + 1 < rows:
                    below = grid[r + 1][c]
                    
                    if below == '|':
                        # Can go straight down
                        dp[r + 1][c] += dp[r][c]
                    elif below == '^':
                        # Skip the ^ row, go to | cells two rows down diagonally
                        # Left diagonal
                        if c - 1 >= 0 and r + 2 < rows and grid[r + 2][c - 1] == '|':
                            dp[r + 2][c - 1] += dp[r][c]
                        # Right diagonal
                        if c + 1 < cols and r + 2 < rows and grid[r + 2][c + 1] == '|':
                            dp[r + 2][c + 1] += dp[r][c]
    
    # Count all paths that reached the last row
    total_paths = 0
    for c in range(cols):
        if grid[rows - 1][c] == '|':
            total_paths += dp[rows - 1][c]
    
    return total_paths


if __name__ == "__main__":       
    result = solve_paths("output.txt")
    print(f"Number of possible paths: {result}")