from collections import deque

class Graph:
    def __init__(self):
        # Adjacency list: {Material: [(NeighborMaterial, weight), ...]}
        self.adjacency = {}

    def add_node(self, material):
        """Ensure node exists in adjacency list."""
        if material not in self.adjacency:
            self.adjacency[material] = []

    def add_edge(self, mat1, mat2, weight=1):
        """
        Add an undirected weighted edge between mat1 and mat2.
        Avoids duplicate edges by checking existing neighbors.
        """
        self.add_node(mat1)
        self.add_node(mat2)

        # Insert edge mat1 -> mat2 if not already present
        if not any(n == mat2 for n, _ in self.adjacency[mat1]):
            self.adjacency[mat1].append((mat2, weight))

        # Insert edge mat2 -> mat1 if not already present
        if not any(n == mat1 for n, _ in self.adjacency[mat2]):
            self.adjacency[mat2].append((mat1, weight))

    def get_neighbors(self, material):
        """Return list of (neighbor, weight) pairs for a given material."""
        return self.adjacency.get(material, [])

    def bfs(self, start, max_depth=None):
        """
        Breadth-first search:
        Returns list of tuples (Material, depth) representing the
        order and distance at which nodes are discovered.
        """
        if start not in self.adjacency:
            return []

        visited = set()
        queue = deque([(start, 0)])
        result = []

        while queue:
            node, depth = queue.popleft()

            if node in visited:
                continue

            visited.add(node)
            result.append((node, depth))

            # Stop expanding if depth limit reached
            if max_depth is not None and depth >= max_depth:
                continue

            # Add neighbors to queue
            for neighbor, _ in self.adjacency[node]:
                if neighbor not in visited:
                    queue.append((neighbor, depth + 1))

        return result

    def __len__(self):
        """Return number of nodes in graph."""
        return len(self.adjacency)
