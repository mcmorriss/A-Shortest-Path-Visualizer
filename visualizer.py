import pygame
import math
from queue import PriorityQueue
pygame.font.init()

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A-Star Path Finding Algorithm")

TEXT_FONT = pygame.font.SysFont('ariel', 35)
TEXT_FONT_2 = pygame.font.SysFont('ariel', 25)
ORANGE_FONT = pygame.font.SysFont('ariel', 25)
TURQ_FONT = pygame.font.SysFont('ariel', 25)
GREEN_FONT = pygame.font.SysFont('ariel', 25)
RED_FONT = pygame.font.SysFont('ariel', 25)

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


class Spot:
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

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

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


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw, start):
    while current in came_from:
        current = came_from[current]
        # Stops path covering start node.
        if current == start:
            break
        current.make_path()
        draw()


def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    # Algorithm runs until open set is empty.
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:  # Reconstruct path if end is found.
            reconstruct_path(came_from, end, draw, start)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()  # Close current node because it has been visited.

    return False  # Path not found.


def make_grid(rows, width):
    grid = []
    gap = width // rows

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Spot(i, j, gap, rows)
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

    pygame.draw.rect(win, BLACK, pygame.Rect(0,675,WIDTH,200))
    instructions = TEXT_FONT.render("Instructions: ", 1, YELLOW)

    instructions_2 = TEXT_FONT_2.render(
        "Left-click once to create the starting node, which will be ",
        1, WHITE)
    orange_text = ORANGE_FONT.render("orange.", 1, ORANGE)

    instructions_3 = TEXT_FONT_2.render(
        "Left-click again to create the end node, which will be ",
        1, WHITE)
    turq_text = TURQ_FONT.render("turquoise.", 1, TURQUOISE)

    instructions_4 = TEXT_FONT_2.render(
        "Optionally, create barriers by dragging the left click, which will be black.",
        1, WHITE)
    instructions_5 = TEXT_FONT_2.render(
        "Then, press the [ Space Bar ] the execute the algorithm.",
        1, WHITE)
    instructions_6 = TEXT_FONT_2.render("Open Node = ", 1, WHITE)
    green_text = GREEN_FONT.render("green", 1, GREEN)
    instructions_7 = TEXT_FONT_2.render("Visited Node = ", 1, WHITE)
    red_text = RED_FONT.render("red", 1, RED)
    win.blit(instructions, (10, 680))
    win.blit(instructions_2, (10, 705))
    win.blit(orange_text, (instructions_2.get_width() + 10, 705))
    win.blit(instructions_3, (10, 725))
    win.blit(turq_text, (instructions_3.get_width() + 10, 725))
    win.blit(instructions_4, (10, 745))
    win.blit(instructions_5, (10, 765))
    win.blit(instructions_6, (instructions_4.get_width() + 30, 705))
    win.blit(green_text, (instructions_4.get_width() + 30 + instructions_6.get_width(), 705))
    win.blit(instructions_7, (instructions_4.get_width() + 30, 725))
    win.blit(red_text, (instructions_4.get_width() + 30 + instructions_7.get_width(), 725))

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

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

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
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

    pygame.quit()


main(WIN, WIDTH)
