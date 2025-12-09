def read_coordinates_from_file(filename):
  
    coordinates = []
    
    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if line:  # Skip empty lines
                    parts = line.split(',')
                    if len(parts) == 2:
                        try:
                            x = int(parts[0].strip())
                            y = int(parts[1].strip())
                            coordinates.append((x, y))
                        except ValueError:
                            print(f"Warning: Skipping invalid line: {line}")
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []
    
    return coordinates

#------------------------------------------------------------------------------------------
def is_inside_rectilinear(px, py, vertices):
    
    n = len(vertices)
    crossings = 0
    p1x, p1y = vertices[-1]
    
    for i in range(n):
        p2x, p2y = vertices[i]
        
        # Only consider vertical edges (p1x == p2x)
        if p1x == p2x:
            # Check if the edge is to the right of the point (p1x > px)
            if p1x > px:
                y_min = min(p1y, p2y)
                y_max = max(p1y, p2y)
                
                # Check if the ray at py intersects the vertical edge
                # We use the half-open interval [y_min, y_max) to handle vertices correctly
                if y_min <= py < y_max:
                    crossings += 1
        
        p1x, p1y = p2x, p2y
    
    return crossings % 2 == 1

def precompute_polygon_grid(polygon_vertices):
    
    # 1. Collect and sort unique coordinates
    all_x = sorted(list(set(v[0] for v in polygon_vertices)))
    all_y = sorted(list(set(v[1] for v in polygon_vertices)))
    
    x_map = {x: i for i, x in enumerate(all_x)}
    y_map = {y: i for i, y in enumerate(all_y)}
    
    num_cols = len(all_x) - 1
    num_rows = len(all_y) - 1
    
    if num_rows <= 0 or num_cols <= 0:
        return None, None, None, None

    # 2. Create the simple grid (1=Inside, 0=Outside)
    simple_grid = [[0] * num_cols for _ in range(num_rows)]
    for r in range(num_rows):
        cy = (all_y[r] + all_y[r+1]) / 2
        for c in range(num_cols):
            cx = (all_x[c] + all_x[c+1]) / 2
            if is_inside_rectilinear(cx, cy, polygon_vertices):
                simple_grid[r][c] = 1

    # 3. Create the 2D Prefix Sum Array (Summed-Area Table)
    # prefix_sum_grid[r][c] stores the sum of all values in simple_grid[0..r-1][0..c-1]
    prefix_sum_grid = [[0] * (num_cols + 1) for _ in range(num_rows + 1)]
    for r in range(1, num_rows + 1):
        for c in range(1, num_cols + 1):
            prefix_sum_grid[r][c] = (
                simple_grid[r-1][c-1] + 
                prefix_sum_grid[r-1][c] + 
                prefix_sum_grid[r][c-1] - 
                prefix_sum_grid[r-1][c-1]
            )
            
    return prefix_sum_grid, x_map, y_map, all_x, all_y

def is_rectangle_fully_inside_optimized(x1, y1, x2, y2, precomputed_data):
    
    prefix_sum_grid, x_map, y_map, all_x, all_y = precomputed_data
    
    # Map geometric coordinates to grid indices
    min_x, max_x = min(x1, x2), max(x1, x2)
    min_y, max_y = min(y1, y2), max(y1, y2)
    
    # Find the indices of the elementary cells that make up the rectangle
    # The rectangle [min_x, max_x] x [min_y, max_y] covers cells starting at:
    # row index: y_map[min_y]
    # col index: x_map[min_x]
    # and ending at:
    # row index: y_map[max_y] - 1
    # col index: x_map[max_x] - 1
    
    try:
        r_start = y_map[min_y]
        r_end = y_map[max_y] # Exclusive end index for prefix sum
        c_start = x_map[min_x]
        c_end = x_map[max_x] # Exclusive end index for prefix sum
    except KeyError:
        # If the coordinates are not on the grid lines, the rectangle is not valid
        # for this problem's geometric constraints.
        return False

    # The number of cells in the sub-rectangle
    num_cells = (r_end - r_start) * (c_end - c_start)
    if num_cells <= 0:
        return False

    # Calculate the sum of the sub-rectangle using the prefix sum array
    # Sum(r_start..r_end-1, c_start..c_end-1)
    sub_rect_sum = (
        prefix_sum_grid[r_end][c_end]
        - prefix_sum_grid[r_start][c_end]
        - prefix_sum_grid[r_end][c_start]
        + prefix_sum_grid[r_start][c_start]
    )
    
    # The rectangle is fully inside if the sum of its cells equals the number of cells
    return sub_rect_sum == num_cells

def find_largest_rectangle_area_constrained_optimized(coordinates, polygon_vertices):
    
    # Pre-computation: O(M * N * V)
    precomputed_data = precompute_polygon_grid(polygon_vertices)
    if precomputed_data[0] is None:
        return 0
        
    max_area_user_formula = 0
    best_points = None
    
    n = len(coordinates)
    
    # Outer Loop: O(N^2)
    for i in range(n):
        x1, y1 = coordinates[i]
        
        for j in range(i + 1, n):
            x2, y2 = coordinates[j]
            
            # 1. Optimized Check for polygon containment: O(1)
            if is_rectangle_fully_inside_optimized(x1, y1, x2, y2, precomputed_data):
                
                # 2. Calculate area using the user's formula
                width_user = abs(x2 - x1) + 1
                height_user = abs(y2 - y1) + 1
                area_user = width_user * height_user
                
                if area_user > max_area_user_formula:
                    max_area_user_formula = area_user
                    best_points = ((x1, y1), (x2, y2))
    
    return max_area_user_formula, best_points

if __name__ == "__main__":
    test_vertices = read_coordinates_from_file("input.txt")

    potential_corners = test_vertices

    max_area, best_points = find_largest_rectangle_area_constrained_optimized(potential_corners, test_vertices)

    #print(f"Polygon Vertices: {test_vertices}")    
    print(f"Opposite corners: {best_points[0]} and {best_points[1]}")

    x1, y1 = best_points[0]
    x2, y2 = best_points[1]

    width_user = abs(x2 - x1) + 1
    height_user = abs(y2 - y1) + 1

    print(f"Width  : {width_user}")
    print(f"Height : {height_user}")
    print(f"Area   : {max_area}")
