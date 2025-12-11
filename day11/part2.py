def load_graph(filename):
    graph = {}
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            src, dsts = line.split(":")
            src = src.strip()
            next_nodes = dsts.strip().split()
            graph[src] = next_nodes
    return graph


def count_paths_with_requirements(graph, start, target, required):
    # Assign each required node a bit position
    required_index = {node: i for i, node in enumerate(required)}
    required_mask_full = (1 << len(required)) - 1

    memo = {}  # memo[(node, mask)] = number of valid paths

    def dfs(node, mask):
        key = (node, mask)
        if key in memo:
            return memo[key]

        # If node is required, set its bit in mask
        if node in required_index:
            mask |= (1 << required_index[node])

        # If we reached target, only count if all required nodes were visited
        if node == target:
            return 1 if mask == required_mask_full else 0

        # No outgoing edges → dead end
        if node not in graph:
            return 0

        total = 0
        for nxt in graph[node]:
            total += dfs(nxt, mask)

        memo[key] = total
        return total

    return dfs(start, 0)


def main(filename):
    graph = load_graph(filename)
    
    start = "svr"
    target = "out"
    required_nodes = ["dac", "fft"]

    count = count_paths_with_requirements(graph, start, target, required_nodes)

    print(f"Number of paths from {start} to {target} that include {required_nodes}: {count}")


if __name__ == "__main__":
    #main("test.txt")
    main("input.txt")