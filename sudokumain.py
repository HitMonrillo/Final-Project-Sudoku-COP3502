#Main file where everything will be running#
import sys
import random
#Seems like we can use random to randomize our boards somehow
import pygame

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Sudoku')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        pygame.display.update()
