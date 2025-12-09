class Graph:
    def __init__(self):
        # adjacency list structure
        # key: Material object
        # value: list of (neighbor_material, weight)
        self.adjacency = {}

    def add_node(self, material):
        """Add a material as a graph node if not already present."""
        if material not in self.adjacency:
            self.adjacency[material] = []

    def add_edge(self, mat1, mat2, weight=1):
        """Add undirected edge with similarity weight."""
        self.add_node(mat1)
        self.add_node(mat2)

        # Prevent duplicate edges
        if not any(neighbor == mat2 for neighbor, _ in self.adjacency[mat1]):
            self.adjacency[mat1].append((mat2, weight))

        if not any(neighbor == mat1 for neighbor, _ in self.adjacency[mat2]):
            self.adjacency[mat2].append((mat1, weight))

    def get_neighbors(self, material):
        """Return list of (neighbor, weight) if exists."""
        return self.adjacency.get(material, [])

    def __len__(self):
        """Return number of nodes in graph."""
        return len(self.adjacency)
