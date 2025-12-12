# datastructures/graph.py

from collections import defaultdict, deque
import numpy as np


class Graph:
    def __init__(self):
        # adjacency list: material → list of (neighbor, weight)
        self.adj = defaultdict(list)


    def compute_similarity(self, m1, m2):
        # Density similarity
        if m1.density is None or m2.density is None:
            density_sim = 0.0
        else:
            diff = abs(m1.density - m2.density)
            density_sim = max(0, 1 - diff / 10)

        # Moment similarity
        try:
            if np.isnan(m1.moment) or np.isnan(m2.moment):
                moment_sim = 0.0
            else:
                mdiff = abs(m1.moment - m2.moment)
                moment_sim = max(0, 1 - mdiff / 10)
        except:
            moment_sim = 0.0

        # Space group match already guaranteed
        sg_sim = 1.0

        # Total similarity range: 0–3
        return density_sim + moment_sim + sg_sim


    def add_edge(self, m1, m2, weight):
        self.adj[m1].append((m2, weight))
        self.adj[m2].append((m1, weight))


    def build_similarity_graph(self, materials, threshold=2):
        # 1. Group materials by space group number
        sg_groups = defaultdict(list)
        for m in materials:
            sg_groups[m.space_group.number].append(m)

        edges_created = 0

        # 2. Compare pairwise ONLY inside each space group bucket
        for sg, group in sg_groups.items():
            n = len(group)
            if n < 2:
                continue  # cannot form edges

            for i in range(n):
                for j in range(i + 1, n):
                    m1, m2 = group[i], group[j]

                    # Compute similarity (SG match guaranteed here)
                    sim = self.compute_similarity(m1, m2)

                    # Create an edge if similarity passes threshold
                    if sim >= threshold:
                        self.add_edge(m1, m2, sim)
                        edges_created += 1

        return edges_created

    def build_local_similarity_graph(self, materials, target, threshold=2):
        target_sg = target.space_group.number
        same_sg = [m for m in materials if m.space_group.number == target_sg]
        edges_created = 0
        for m in same_sg:
            if m is target:
                continue
            sim = self.compute_similarity(target, m)
            if sim >= threshold:
                self.add_edge(target, m, sim)
                edges_created += 1
        return edges_created

    def bfs(self, start):
        visited = set()
        queue = deque([start])
        visited.add(start)

        while queue:
            node = queue.popleft()
            for neighbor, _ in self.adj[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return visited

    def summary(self):
        print(f"Graph has {len(self.adj)} materials.")
        edge_count = sum(len(v) for v in self.adj.values()) // 2
        print(f"Graph has {edge_count} undirected edges.")
