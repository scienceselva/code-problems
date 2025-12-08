import math
import sys

# for DSU
sys.setrecursionlimit(2000)

class DSU:
    # Disjoint Set Union (Union-Find) data structure with path compression and union by size.
    def __init__(self, n):
        # parent[i] stores the parent of element i. If parent[i] == i, i is the root.
        self.parent = list(range(n))
        # size[i] stores the size of the set rooted at i. Only meaningful if i is a root.
        self.size = [1] * n
        # Tracks the number of disjoint sets (circuits)
        self.num_sets = n

    def find(self, i):
        # Finds the representative (root) of the set containing i, with path compression.
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        # Unites the sets containing i and j, using union by size.
        root_i = self.find(i)
        root_j = self.find(j)

        if root_i != root_j:
            # Union by size: attach smaller tree to root of larger tree
            if self.size[root_i] < self.size[root_j]:
                root_i, root_j = root_j, root_i

            self.parent[root_j] = root_i
            self.size[root_i] += self.size[root_j]
            self.num_sets -= 1 # Decrement the number of sets
            return True  # Union successful
        return False # Already in the same set

def parse_coordinates(file_path):
    # Reads and parses the coordinates from the input file.
    coordinates = []
    with open(file_path, 'r') as f:
        for line in f:
            try:
                x, y, z = map(int, line.strip().split(','))
                coordinates.append((x, y, z))
            except ValueError:                
                continue
    return coordinates

def squared_distance(p1, p2):
    return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2

def solve_last_connection(file_path):
    coordinates = parse_coordinates(file_path)
    N = len(coordinates)
    
    if N < 2:
        raise ValueError("Need at least 2 junction boxes to form a circuit.")

    # 1. Generate all possible edges with squared distances
    # Store (distance, index1, index2)
    edges = []
    for i in range(N):
        for j in range(i + 1, N):
            dist_sq = squared_distance(coordinates[i], coordinates[j])
            edges.append((dist_sq, i, j))

    # 2. Sort edges by distance (Kruskal's algorithm)
    edges.sort(key=lambda x: x[0])

    # 3. Initialize DSU structure
    dsu = DSU(N)
    
    last_connected_pair_indices = None

    # 4. Process edges until only one set remains
    for _, i, j in edges:
        # Attempt to connect the two junction boxes
        if dsu.union(i, j):
            # Union was successful, meaning a new connection was made
            last_connected_pair_indices = (i, j)
            
            # Check if all boxes are now in a single circuit
            if dsu.num_sets == 1:
                break
    
    if dsu.num_sets > 1:
        raise RuntimeError("Could not connect all coordinates into a single group.")

    # 5. Extract the X-coordinates of the last connected pair
    idx1, idx2 = last_connected_pair_indices
    x1 = coordinates[idx1][0]
    x2 = coordinates[idx2][0]
    
    product = x1 * x2

    print(f"Total junction boxes (N): {N}")
    print(f"Last connected pair indices: {idx1}, {idx2}")
    print(f"Last connected pair coordinates: {coordinates[idx1]}, {coordinates[idx2]}")
    print(f"X-coordinates: {x1}, {x2}")
    print(f"Product of X-coordinates: {product}")
    
    return product

if __name__ == "__main__":
    
    try:
        result = solve_last_connection("coordinates.txt")
    except Exception as e:
        print(f"An error occurred: {e}")
