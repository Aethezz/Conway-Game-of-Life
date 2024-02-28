import time
import pygame
import numpy as np

pygame.init()

background_colour = (130, 130, 130)
grid_colour = (0, 0, 0)
tile_colour = (173, 216, 230)

width, height = 600, 600
tile_size = 15
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

def main():
    ongoing = True
    dragging = False
    right = left = False
    locations = set()
    
    while ongoing:
        time.tick(fps)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ongoing = False
        
            elif event.type == pygame.MOUSEBUTTONDOWN:
                dragging = True
                if event.button == 1:
                    left = True
                elif event.button == 3:
                    right = True
            
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = left = right = False

            if event.type == pygame.MOUSEMOTION:
                if dragging and left:
                    
                    x, y = pygame.mouse.get_pos()
                    col = x // tile_size
                    row = y // tile_size    
                    pos = (col, row)

                    if pos not in locations:
                        locations.add(pos)
                
                if dragging and right:
                    x, y = pygame.mouse.get_pos()
                    col = x // tile_size
                    row = y // tile_size    
                    pos = (col, row)
                    
                    if pos in locations:
                        locations.remove(pos)
                    
        window.fill(background_colour)
        grid(locations)
        pygame.display.update()
        
    pygame.quit()

if __name__ == "__main__":
    main()