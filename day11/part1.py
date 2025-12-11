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


def find_all_paths(graph, start, target="out"):
    """
    Iterative DFS that finds all distinct paths from start -> target.
    Prevents cycles by tracking visited nodes per-path.
    """
    all_paths = []
    stack = [(start, [start])]  # (current_node, path_so_far)

    while stack:
        node, path = stack.pop()

        # reached "out"
        if node == target:
            all_paths.append(path)
            continue

        # if node not in graph → dead end
        if node not in graph:
            continue

        for nxt in graph[node]:
            if nxt not in path:  # prevents cycles
                stack.append((nxt, path + [nxt]))

    return all_paths


def main(filename):
    graph = load_graph(filename)

    start = "you"
    target = "out"

    paths = find_all_paths(graph, start, target)

    print("\nAll paths from", start, "to", target, ":\n")
    for p in paths:
        print(" -> ".join(p))

    print("\nTotal paths:", len(paths))


if __name__ == "__main__":
    #main("test.txt")
    main("input.txt")