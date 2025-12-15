from collections import deque
import numpy as np


class Graph:
    def __init__(self):

        #Init empty graph, nodes stores all materials, and adj stores all neighbors
        self.nodes = []
        self.adj = []


    def _add_node(self, m):

        #Check if material is already in list, if not add
        if m not in self.nodes:
            self.nodes.append(m)
            self.adj.append([])


    def _compute_similarity(self, m1, m2):
        #Calculate similarity score between two materials


        #Density Similarity
        #Handle 0 values for density, assign 0 score
        if m1.density is None or m2.density is None:
            density_sim = 0.0

        
        else:
            #Calculate absolute value of density delta
            #Score from 0->1:  1-(|delta| / 10),closer  to 1 is higher similarity 
            diff = abs(m1.density - m2.density)
            density_sim = max(0, 1 - diff / 10)

        #Moment similarity
        #Handle missing or non number values for Moment, assign 0 score
        try:
            if np.isnan(m1.moment) or np.isnan(m2.moment):
                moment_sim = 0.0

            
            else:
                #Calculate absolute value of moment delta
                #Score from 0->1: 1-(|delta| / 10), closer to 1 is higher similarity
                mdiff = abs(m1.moment - m2.moment)
                moment_sim = max(0, 1 - mdiff / 10)

        #Assign 0 score if error from pulling moment
        except:
            moment_sim = 0.0
            
        #Assign similar space group score to 1
        sg_sim = 1.0

        #Final Score: Add density, moment, and spacegroup score
        return density_sim + moment_sim + sg_sim


    def _add_edge(self, m1, m2, weight):
        #Build edges with similarity score
        
        #Ensure both materials exist in the graph
        self._add_node(m1)
        self._add_node(m2)

        #Get index for each material
        i = self.nodes.index(m1)
        j = self.nodes.index(m2)

        #Add undirected edge between each material
        self.adj[i].append((j, weight))
        self.adj[j].append((i, weight))


    def build_similarity_graph(self, materials, threshold=2):
        #Build similarity graph(just nodes) for all materials
        for m in materials:
            self._add_node(m)

        edges_created = 0
        n = len(materials)

        #Compare each unique value once
        for i in range(n):
            for j in range(i + 1, n):
                m1, m2 = materials[i], materials[j]

                #Skip if space group does not match
                if m1.space_group.number != m2.space_group.number:
                    continue

                #Compute similarity 
                sim = self._compute_similarity(m1, m2)

                #Create an edge if similarity passes threshold
                if sim >= threshold:
                    self._add_edge(m1, m2, sim)
                    edges_created += 1

        return edges_created


    def build_local_similarity_graph(self, materials, target, threshold=2):
        
        #Add only target material as a node
        self._add_node(target)
        edges_created = 0

        for m in materials:
            if m is target:
                continue

            #Only compare materials in same space group
            if m.space_group.number != target.space_group.number:
                continue

            sim = self._compute_similarity(target, m)

            #Create edge if similarity passes threshold
            if sim >= threshold:
                self._add_edge(target, m, sim)
                edges_created += 1

        return edges_created


    def bfs(self, start):
        #Discover all materials that are connected through similarity
        visited = set()
        queue = deque()

        #Convert starting material to index
        start_idx = self.nodes.index(start)
        visited.add(start_idx)
        queue.append(start_idx)

        while queue:
            idx = queue.popleft()

            #Visit neighbors of current node
            for neighbor_idx, _ in self.adj[idx]:
                if neighbor_idx not in visited:
                    visited.add(neighbor_idx)
                    queue.append(neighbor_idx)

        #Return actual material objects
        return {self.nodes[i] for i in visited}


    def summary(self):
        print(f"Graph has {len(self.nodes)} materials.")
        edge_count = sum(len(v) for v in self.adj) // 2
        print(f"Graph has {edge_count} undirected edges.")
