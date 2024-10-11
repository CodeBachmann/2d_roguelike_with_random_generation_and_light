import heapq

class Node:
    def __init__(self, position, g_cost, h_cost, parent=None):
        self.position = position
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.f_cost = g_cost + h_cost
        self.parent = parent

    def __lt__(self, other):
        return self.f_cost < other.f_cost

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

import heapq
import time

def a_star(grid, start, goal, timeout):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_neighbors(pos):
        x, y = pos
        neighbors = []
        directions = [
            (0, 1), (1, 0), (0, -1), (-1, 0),  # Orthogonal
            (1, 1), (1, -1), (-1, 1), (-1, -1)  # Diagonal
        ]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid) and grid[ny][nx] == 0:
                if dx != 0 and dy != 0:  # Diagonal move
                    # Check if both adjacent cells are walkable
                    if grid[y][nx] == 0 and grid[ny][x] == 0:
                        neighbors.append((nx, ny))
                else:  # Orthogonal move
                    neighbors.append((nx, ny))
        return neighbors

    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set and time.time() < timeout:
        current = heapq.heappop(open_set)[1]

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        for neighbor in get_neighbors(current):
            tentative_g_score = g_score[current] + 1

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None  # Path not found within the timeout