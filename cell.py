import pygame

class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.sketched_value = 0
        self.row = row
        self.col = col
        self.screen = screen
        self.selected = False

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value

    def draw(self):
        font = pygame.font.SysFont('Arial', 24)
        if self.value != 0:
            text = font.render(str(self.value), True, pygame.Color('black'))
            self.screen.blit(text, (self.col * 60 + 20, self.row * 60 + 15))
        elif self.sketched_value != 0:
            text = font.render(str(self.sketched_value), True, pygame.Color('gray'))
            self.screen.blit(text, (self.col * 60 + 5, self.row * 60 + 5))
        if self.selected:
            pygame.draw.rect(self.screen, pygame.Color('red'), (self.col * 60, self.row * 60, 60, 60), 3)
