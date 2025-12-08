import math
import sys

# for DSU
sys.setrecursionlimit(2000)

class DSU:
    #Disjoint Set Union (Union-Find) data structure with path compression and union by size.
    def __init__(self, n):
        # parent[i] stores the parent of element i. If parent[i] == i, i is the root.
        self.parent = list(range(n))
        # size[i] stores the size of the set rooted at i. Only meaningful if i is a root.
        self.size = [1] * n

    def find(self, i):
        #Finds the representative (root) of the set containing i, with path compression.
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        #Unites the sets containing i and j, using union by size.
        root_i = self.find(i)
        root_j = self.find(j)

        if root_i != root_j:
            # Union by size: attach smaller tree to root of larger tree
            if self.size[root_i] < self.size[root_j]:
                root_i, root_j = root_j, root_i

            self.parent[root_j] = root_i
            self.size[root_i] += self.size[root_j]
            return True  # Union successful
        return False # Already in the same set

def parse_coordinates(file_path):
    #Reads and parses the coordinates from the input file.
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

def solve_circuit_problem(file_path, num_connections):

    coordinates = parse_coordinates(file_path)
    N = len(coordinates)
    
    if N < 3:
        raise ValueError("Need at least 3 to find three largest group.")

    # 1. Generate all possible edges with squared distances
    edges = []
    for i in range(N):
        for j in range(i + 1, N):
            dist_sq = squared_distance(coordinates[i], coordinates[j])
            edges.append((dist_sq, i, j))

    # 2. Sort edges by distance
    edges.sort(key=lambda x: x[0])

    # 3. Initialize DSU structure
    dsu = DSU(N)

    # 4. Process the shortest 'num_connections' edges
    # The problem is to consider the 1000 shortest *pairs*, regardless of whether they
    # form a successful union.
    edges_to_process = edges[:num_connections]
    
    for _, i, j in edges_to_process:
        # Attempt to connect the two junction boxes
        dsu.union(i, j)

    # 5. Calculate the size of each circuit
    circuit_sizes = {}
    for i in range(N):
        root = dsu.find(i)
        # We only need to check the size of the root once.
        # The DSU.size array stores the size of the set for the root element.
        if root not in circuit_sizes:
            circuit_sizes[root] = dsu.size[root]

    # 6. Find the three largest circuit sizes
    sizes = sorted(circuit_sizes.values(), reverse=True)

    if len(sizes) < 3:
        # This should not happen if N >= 3, but as a safeguard
        raise ValueError(f"Only {len(sizes)} circuits found. Cannot find three largest.")

    # 7. Calculate the product of the three largest sizes
    top_three_sizes = sizes[:3]
    product = top_three_sizes[0] * top_three_sizes[1] * top_three_sizes[2]

    print(f"Total junction boxes (N): {N}")
    print(f"Total edges generated: {len(edges)}")
    print(f"Number of shortest connections processed: {num_connections}")
    print(f"All circuit sizes: {sizes}")
    print(f"Three largest circuit sizes: {top_three_sizes}")
    print(f"Product of the three largest circuit sizes: {product}")
    
    return product

if __name__ == "__main__":    
    try:
        result = solve_circuit_problem("input.txt", 1000)
    except Exception as e:
        print(f"An error occurred: {e}")
