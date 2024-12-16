from solution_base import SolutionBase
from typing import TextIO
from heapq import heappush, heappop

class Link:
    def __init__(self, node: 'Node', distance: int):
        self.node = node
        self.distance = distance

class Node:
    def __init__(self, key: tuple[int, int, str], is_end: bool):
        self.key = key
        self.neighbors: dict[tuple[int, int, str], Link] = {}
        self.is_end = is_end
    
    def add_neighbor(self, neighbor: 'Node', distance: int):
        self.neighbors[neighbor.key] = Link(neighbor, distance)
        neighbor.neighbors[self.key] = Link(self, distance)


class Solution(SolutionBase):
    def read_input(self, file: TextIO):
        self.nodes: dict[tuple[int, int, str], Node] = {}
        self.start: tuple[int, int, str] = (0, 0, "right")
        self.end: tuple[int, int] = (0, 0)

        self.map: list[str] = []
        
        for line in file:
            self.map.append(line.strip())
        
    def build_graph(self):
        self.nodes: dict[tuple[int, int, str], Node] = {}
        self.start: tuple[int, int, str] = (0, 0, "right")

        for y, row in enumerate(self.map):
            for x, char in enumerate(row):
                if char == '#':
                    continue
                
                if char == 'S':
                    self.start = (x, y, "right")
                
                is_end = char == 'E'
                if is_end:
                    self.end = (x, y)
                self.nodes[(x, y, "up")] = Node((x, y, "up"), is_end)
                self.nodes[(x, y, "down")] = Node((x, y, "down"), is_end)
                self.nodes[(x, y, "left")] = Node((x, y, "left"), is_end)
                self.nodes[(x, y, "right")] = Node((x, y, "right"), is_end)
    
        for pos, node in self.nodes.items():
            x, y, direction = pos
            if direction == "up" or direction == "down":
                node.add_neighbor(self.nodes[(x, y, "right")], 1000)
                node.add_neighbor(self.nodes[(x, y, "left")], 1000)
            if direction == "left" or direction == "right":
                node.add_neighbor(self.nodes[(x, y, "up")], 1000)
                node.add_neighbor(self.nodes[(x, y, "down")], 1000)
                
            match direction:
                case "up":
                    neighbor_pos = (x, y - 1, "up")
                case "down":
                    neighbor_pos = (x, y + 1, "down")
                case "left":
                    neighbor_pos = (x - 1, y, "left")
                case "right":
                    neighbor_pos = (x + 1, y, "right")
                
            neighbor = self.nodes.get(neighbor_pos, None)
            if neighbor is not None:
                node.add_neighbor(neighbor, 1)
    
    def dijkstra(self):
        distances: dict[tuple[int, int, str], int] = {}
        previous: dict[tuple[int, int, str], list[tuple[int, int, str]]] = {}
        queue: list[tuple[int, tuple[int, int, str]]] = []
        
        processed = set()
        
        for key in self.nodes:
            distances[key] = float('inf')
            previous[key] = []
        
        distances[self.start] = 0
        heappush(queue, (0, self.start))
        
        while queue:            
            current_distance, current_key = heappop(queue)
            
            if current_key in processed:
                continue
            
            processed.add(current_key)
            node = self.nodes[current_key]

            for link in node.neighbors.values():
                if link.node.key in processed:
                    continue
                
                alt = current_distance + link.distance
                if alt < distances[link.node.key]:
                    distances[link.node.key] = alt
                    previous[link.node.key] = [current_key]
                    heappush(queue, (alt, link.node.key))
                elif alt == distances[link.node.key]:
                    previous[link.node.key].append(current_key)
        
        return distances, previous
    
    def find_shortest_path_length(self, distances: dict[tuple[int, int, str], int]) -> int:
        ends = [distances[(self.end[0], self.end[1], direction)] for direction in ["up", "down", "left", "right"]]
        return min(ends)
    
    def part_one(self):
        self.build_graph()
        
        distances, _ = self.dijkstra()
        return self.find_shortest_path_length(distances)

    def find_seats(self, previous: dict[tuple[int, int, str], list[tuple[int, int, str]]], ends: list[tuple[int, int, str]]) -> set[tuple[int, int]]:
        # Seats don't have a direction.
        seats: set[tuple[int, int]] = set()

        visited: set[tuple[int, int, str]] = set([end for end in ends])
        queue: list[tuple[int, int, str]] = [end for end in ends]
        
        while queue:
            current_key = queue.pop(0)
            seats.add((current_key[0], current_key[1]))
            
            for prev in previous[current_key]:
                if prev not in visited:
                    queue.append(prev)
                    visited.add(prev)
        
        return seats

    def part_two(self):
        self.build_graph()
        distances, previous = self.dijkstra()
        shortest_path_length = self.find_shortest_path_length(distances)

        ends = [(self.end[0], self.end[1], direction) for direction in ["up", "down", "left", "right"] if distances[(self.end[0], self.end[1], direction)] == shortest_path_length]
        
        seats = self.find_seats(previous, ends)
            
        return len(seats)
