from solution_base import SolutionBase
from typing import TextIO

class Solution(SolutionBase):
    def read_input(self, file: TextIO):
        self.graph: dict[str, set[str]] = {}
        self.biggest_clique: set[str] = set()
        self.biggest_clique_size: int = 0
        
        for line in file:
            l, r = line.strip().split("-")
            if l not in self.graph:
                self.graph[l] = set()
            if r not in self.graph:
                self.graph[r] = set()

            self.graph[l].add(r)
            self.graph[r].add(l)
    
    # Find group of 3 computers connected to each other
    def part_one(self) -> int:
        self.groups: set[tuple[str, str, str]] = set()

        for node in self.graph:
            for neighbor in self.graph[node]:
                for neighbor_of_neighbor in self.graph[neighbor]:
                    if node in self.graph[neighbor_of_neighbor]:
                        sorted_group = sorted([node, neighbor, neighbor_of_neighbor])
                        self.groups.add(tuple(sorted_group))

        groups_with_computer_starting_with_t = 0
        for group in self.groups:
            for node in group:
                if node.startswith("t"):
                    groups_with_computer_starting_with_t += 1
                    break

        return groups_with_computer_starting_with_t

    def bron_kerbosch_with_pivot(self, R: set[str], P: set[str], X: set[str]):
        """
        Bron-Kerbosch algorithm optimized with pivoting.
        R: Current clique (set of nodes)
        P: Potential candidates (set of nodes)
        X: Already processed nodes (set of nodes)
        """
        if not P and not X:
            if len(R) > self.biggest_clique_size:
                self.biggest_clique_size = len(R)
                self.biggest_clique = R
            return
        
        # Choose a pivot node u from P ∪ X
        u = next(iter(P.union(X))) if P.union(X) else None
        
        # Nodes to consider (P \ N(u))
        for v in list(P.difference(self.graph[u] if u else set())):
            self.bron_kerbosch_with_pivot(R.union({v}), P.intersection(self.graph[v]), X.intersection(self.graph[v]))
            P.remove(v)
            X.add(v)

    # Find the biggest interconnected group
    def part_two(self):
        self.bron_kerbosch_with_pivot(set(), set(self.graph.keys()), set())

        return ",".join(sorted(self.biggest_clique))
