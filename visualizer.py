# Author: Michael Morriss
# Date: July 25th, 2022
# Description: This is a program that uses the pygame visual library to display a live
# visualization of the A* (A-star) shortest path algorithm. The user is able to select
# their own start/end coordinates on a 50 x 50 grid, as well as able to draw borders
# on the grid to increase the difficulty of the path.


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
        self.color = TURQUOISE

    def make_start(self):
        self.color = ORANGE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []

        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # Down
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # Up
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # Right
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # Left
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


def heuristic(p1, p2):
    x1, y1 = p1
    x2, y2, = p2
    return abs(x1 - x2) + abs(y1 - y2)


def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))

    came_from = {}

    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0

    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = heuristic(start.get_pos(), end.get_pos())


def make_grid(rows, width):
    grid = []
    gap = width // rows

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    # Fills the screen.
    win.fill(WHITE)

    # Draw and color all nodes on grid.
    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    started = False

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue

            # If left mouse button is pressed:
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]

                # Creates start node if not already made.
                if not start and spot != end:
                    start = spot
                    start.make_start()

                # Creates end node if not already made.
                elif not end and spot != start:
                    end = spot
                    end.make_end()

                # Colors barrier nodes.
                elif spot != end and spot != start:
                    spot.make_barrier()

            # If right mouse button is pressed:
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors()

                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

    pygame.quit()


main(WIN, WIDTH)





