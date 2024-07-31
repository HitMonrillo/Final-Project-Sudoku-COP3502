# Main file where everything will be running#
import sys
import random

# Seems like we can use random to randomize our boards somehow
import pygame


def draw_button(surface, color, rect, text, text_color, font):
    pygame.draw.rect(surface, color, rect)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)


def create_surface(surface, text, font, color, center):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=center)
    surface.blit(text_surface, text_rect)


def game_start(screen):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    WIDTH = 800
    HEIGHT = 800
    RED = (255, 0, 0)

    start_title_font = pygame.font.Font(None, 75)
    game_mode_font = pygame.font.Font(None, 50)
    button_font = pygame.font.Font(None, 35)

    screen.fill(WHITE)

    create_surface(
        screen,
        "Welcome To Sudoku",
        start_title_font,
        BLACK,
        (WIDTH // 2, HEIGHT // 3 - 150),
    )
    create_surface(
        screen,
        "Select Game Mode:",
        game_mode_font,
        BLACK,
        (WIDTH // 2, HEIGHT // 2 - 100),
    )

    button_rect_1 = pygame.Rect(WIDTH // 3 - 100, HEIGHT // 2, 100, 50)
    button_rect_2 = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2, 100, 50)
    button_rect_3 = pygame.Rect(2 * WIDTH // 3, HEIGHT // 2, 100, 50)

    draw_button(screen, RED, button_rect_1, "Easy", BLACK, button_font)
    draw_button(screen, RED, button_rect_2, "Medium", BLACK, button_font)
    draw_button(screen, RED, button_rect_3, "Hard", BLACK, button_font)

    return button_rect_1, button_rect_2, button_rect_3


pygame.init()

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Sudoku")

button_rect_1, button_rect_2, button_rect_3 = game_start(screen)
pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos  # mouse click position
            if button_rect_1.collidepoint(mouse_pos):
                print("Easy button clicked")  # Create game with easy mode
            elif button_rect_2.collidepoint(mouse_pos):
                print("Medium button clicked")  # Create game with medium mode
            elif button_rect_3.collidepoint(mouse_pos):
                print("Hard button clicked")  # Create game with hard mode

    screen.fill((255, 255, 255))  # clear screen redraw
    button_rect_1, button_rect_2, button_rect_3 = game_start(screen)
    pygame.display.update()
