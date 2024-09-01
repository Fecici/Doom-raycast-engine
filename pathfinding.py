from collections import deque

class Pathfinding:
    def __init__(self, game) -> None:
        self.game = game
        self.map = game.map.tilemap
        self.directions = [-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [1, -1], [1, 1], [-1, 1]
        self.graph = {}

        self.get_graph()

    def get_shortest_path(self, start, goal):
        self.visited = self.bfs(start, goal, self.graph)
        path = [goal]
        step = self.visited.get(goal, start)

        while step and step != start:
            path.append(step)
            step = self.visited[step]
        
        return path[-1]

    def bfs(self, start, goal, graph):

        # this will effectively be the same as every dijkstra approach ive ever used;
        # bfs treats all weights as 1 whereas dijkstra respects edge weights
        queue = deque([start])
        visited = {start: None}

        while len(queue) > 0:
            current_node = queue.popleft()
            if current_node == goal:
                break

            next_nodes = graph[current_node]
            for node in next_nodes:
                if node not in visited and node not in self.game.object_handler.npc_positions:
                    queue.append(node)
                    visited[node] = current_node

        return visited

    def get_next_node(self, x, y):
        allowed = []
        for dx, dy in self.directions:
            if (x + dx, y + dy) not in self.game.map.world_map:  # not a wall
                allowed.append((x + dx, y + dy))
        
        return allowed
    
    def get_graph(self):
        for y, row in enumerate(self.map):
            for x, col in enumerate(row):
                if not col:
                    self.graph[(x, y)] = self.graph.get((x, y), []) + self.get_next_node(x, y)
