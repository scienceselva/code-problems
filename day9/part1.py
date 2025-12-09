def find_largest_rectangle_area(coordinates):

    max_area = 0
    best_points = None
    
    n = len(coordinates)
    
    # Try all pairs of points as potential opposite corners
    for i in range(n):
        x1, y1 = coordinates[i]
        
        for j in range(i + 1, n):
            x2, y2 = coordinates[j]
            
            # Calculate width and height as inclusive cell counts
            width = abs(x2 - x1) + 1
            height = abs(y2 - y1) + 1
            
            # Calculate area
            area = width * height
            
            if area > max_area:
                max_area = area
                best_points = ((x1, y1), (x2, y2))
    
    return max_area, best_points

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

def main():
    # Read coordinates from input file
    input_file = "input.txt"
    coordinates = read_coordinates_from_file(input_file)
    
    # Find the largest rectangle area
    max_area, best_points = find_largest_rectangle_area(coordinates)
    
    if max_area > 0:
        print(f"\nLargest rectangle found!")
        print(f"Opposite corners: {best_points[0]} and {best_points[1]}")
        
        x1, y1 = best_points[0]
        x2, y2 = best_points[1]
        
        # Calculate width and height (inclusive)
        width = abs(x2 - x1) + 1
        height = abs(y2 - y1) + 1
        
        print(f"Width (columns): from {min(x1, x2)} to {max(x1, x2)} = {width} cells")
        print(f"Height (rows): from {min(y1, y2)} to {max(y1, y2)} = {height} cells")
        print(f"Area: {width} × {height} = {max_area}")
 
                
    else:
        print("\nNo rectangle could be formed.")

if __name__ == "__main__":
    main()