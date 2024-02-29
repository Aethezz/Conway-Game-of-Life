import time
import pygame
import numpy as np
import random

pygame.init()

background_colour = (130, 130, 130)
grid_colour = (0, 0, 0)
tile_colour = (173, 216, 230)

width, height = 600, 600
tile_size = 25
grid_width = width // tile_size
grid_height = height // tile_size
fps = 60

window = pygame.display.set_mode((width, height))

time = pygame.time.Clock()

def grid(locations):
    for location in locations:
        col, row = location
        top_left = (col * tile_size, row * tile_size)
        pygame.draw.rect(window, tile_colour, (*top_left, tile_size, tile_size))
    
    for row in range(grid_height):
        pygame.draw.line(window, grid_colour, (0, row * tile_size), (width, row * tile_size))

    for col in range(grid_width):
        pygame.draw.line(window, grid_colour, (col * tile_size, 0), (col * tile_size, height))

def get_pos():
    x, y = pygame.mouse.get_pos()
    col = x // tile_size
    row = y // tile_size
    return (col, row)

def adjust(locations):
    total_neighbours = set()
    new_locations = set()

    # Find number of live neighbours of live cell
    for location in locations:
        live_neighbours = 0
        neighbours = get_neighbours(location)
        total_neighbours.update(neighbours)

        for neighbour in neighbours:
            if neighbour in locations:
                live_neighbours += 1

        if live_neighbours == 2 or live_neighbours == 3:
            new_locations.add(location)
    
    # Find number of live neighbours of dead cell      
    for location in total_neighbours:
        live_neighbours = 0
        neighbours = get_neighbours(location)

        for neighbour in neighbours:
            if neighbour in locations:
                live_neighbours += 1

        if live_neighbours == 3:
            new_locations.add(location)      

    return new_locations 

def get_neighbours(pos):
    x, y = pos
    neighbours = set()

    for deltax in [-1, 0, 1]:
        if x + deltax >= grid_width or x + deltax < 0:
            continue
        for deltay in [-1, 0, 1]:
            if y + deltay >= grid_height or y + deltay < 0:
                continue
            elif deltax == 0 and deltay == 0:
                continue
            
            neighbours.add((x + deltax, y + deltay))
    
    return neighbours

def main():
    ongoing = True
    playing = False
    right_click = left_click = False
    count = 0
    update_frequency = 30

    locations = set()
    
    while ongoing:
        time.tick(fps)
        
        if playing:
            count += 1

        if count >= update_frequency:
            count = 0
            locations = adjust(locations)

        pygame.display.set_caption("Playing" if playing else "Paused")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ongoing = False
        
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    left_click = True
                    pos = get_pos()

                    if pos not in locations:
                        locations.add(pos)
                
                elif event.button == 3:
                    right_click = True
                    pos = get_pos()
                        
                    if pos in locations:
                        locations.remove(pos)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = left_click = right_click = False

            if event.type == pygame.MOUSEMOTION:
                if left_click:
                    pos = get_pos()

                    if pos not in locations:
                        locations.add(pos)
                
                elif right_click:
                    pos = get_pos()
                        
                    if pos in locations:
                        locations.remove(pos)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = not playing

                if event.key == pygame.K_c:
                    locations = set()
                    playing = False
                    count = 0

        window.fill(background_colour)
        grid(locations)
        pygame.display.update()
        
    pygame.quit()

if __name__ == "__main__":
    main()