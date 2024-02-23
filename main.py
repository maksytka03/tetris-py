import pygame
from copy import deepcopy
import random

W, H = 10, 20  # ratio
TILE = 45  # size of a tile in pixels
SC_RES = W * TILE, H * TILE  # screen is 10 tiles wide & 20 tiles tall

pygame.init()
window = pygame.display.set_mode(SC_RES)
clock = pygame.time.Clock()

grid = [pygame.Rect(TILE * x, TILE * y, TILE, TILE) for x in range(W) for y in range(H)]  # Rect takes [x_pos, y_pos, width, height]
figures_pos = {
    "I": [(-2, 0), (-1, 0), (0, 0), (1, 0)],
    "O": [(-1, 0), (0, 0), (-1, 1), (0, 1)],
    "T": [(-2, 0), (-1, 0), (0, 0), (-1, 1)],
    "J": [(0, 0), (0, 1), (0, 2), (-1, 2)],
    "L": [(-1, 0), (-1, 1), (-1, 2), (0, 2)],
    "S": [(-1, 1), (0, 1), (0, 0), (1, 0)],
    "Z": [(-1, 0), (0, 0), (0, 1), (1, 1)],
}
figures = [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in coordinates] for coordinates in figures_pos.values()]  # starting values for tetrominoes
figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)  # TILE - 2 so that the tiles don't fill in a tile entirely
field = [[0 for i in range(W)] for j in range(H)]

figure = deepcopy(random.choice(figures))
count, speed, limit = 0, 60, 2000

def check_borders(figure):
    if figure[i].x < 0 or figure[i].x > W - 1:
        return False
    if figure[i].y > H - 1 or field[figure[i].y][figure[i].x]:
        return False
    return True

while True:
    dx = 0
    rotate = False
    window.fill(pygame.Color("black"))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        elif event.type == pygame.KEYDOWN:  # if key is pressed, check what key it is
            if event.key == pygame.K_LEFT:  # if key is left, do something
                dx += -1  # change the amount of x displacement to negative 1 to move left
            elif event.key == pygame.K_RIGHT:  # elif key is right, do something else
                dx += 1  # change the amount of x displacement to 1 to move right
            elif event.key == pygame.K_DOWN:
                limit = 100
            elif event.key == pygame.K_UP:
                rotate = True

        elif event.type == pygame.KEYUP:
            limit = 2000

    for rect in grid:
        # draw the grid
        pygame.draw.rect(window, (50, 50, 50), rect, 1)  # draw all the "rectangles" with 1 width to make them look like a grid

    figure_old = deepcopy(figure)

    count += speed
    if count > limit:
        count = 0
        for i in range(4):
            figure[i].y += 1
            
            # handle lines
            line = H - 1
            # iterate over all the lines starting from the bottom
            for row in range(H - 1, -1, -1):
                count = sum(field[row])  # count how much of a line is covered
                if count < W:
                    for j in range(W):
                        field[line][j] = field[row][j]
                    line -= 1
                    
            if not check_borders(figure):  # if figure is at the bottom
                for i in range(4):
                    field[figure_old[i].y][figure_old[i].x] = 1
                figure = deepcopy(random.choice(figures))
                break

    # rotation center
    center = figure[1]

    for i in range(4):  # every figure is 4 tiles
        figure[i].x += dx  # increase figure's x coordinates by dx
        if not check_borders(figure):
            figure = figure_old
            break


        if rotate:
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y


        figure_rect.x = figure[i].x * TILE
        figure_rect.y = figure[i].y * TILE
        pygame.draw.rect(window, (255, 255, 0), figure_rect)


    for y, rows in enumerate(field):  # iterate over the field's rows
        for x, col in enumerate(rows):  # iterate over the field's columns
            if col:  # if the column is not empty
                figure_rect.x, figure_rect.y = x * TILE, y * TILE
                pygame.draw.rect(window, "white", figure_rect)

    pygame.display.flip()
    clock.tick(60)
