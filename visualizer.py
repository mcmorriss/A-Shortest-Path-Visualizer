import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A-Star Path Finding Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Node:
    def __init__(self, row, col, width, total_rows):
        """Initialize node variables."""
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        """Returns the x,y coordinates of the current node."""
        return self.row, self.col

    def is_closed(self):
        """Checks if node is red, meaning it's closed."""
        return self.color == RED

    def is_open(self):
        """Checks if node is green, meaning it's open."""
        return self.color == GREEN

    def is_barrier(self):
        """Checks if node is black, meaning it's a barrier."""
        return self.color == BLACK

    def is_start(self):
        """Checks to see if node is the starting node."""
        return self.color == ORANGE

    def is_end(self):
        """Checks to see if node is the ending node."""
        return self.color == TURQUOISE

    def reset(self):
        """Changes node color back to white."""
        self.color = WHITE

    def make_open(self):
        self.color = GREEN

    def make_closed(self):
        self.color = RED

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = PURPLE

    def make_start(self):
        self.color = ORANGE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        pass

    def __lt__(self, other):
        return False


def heuristic(p1, p2):
    x1, y1 = p1
    x2, y2, = p2
    return abs(x1 - x2) + abs(y1 - y2)

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

