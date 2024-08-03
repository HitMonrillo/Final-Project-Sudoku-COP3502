import sys
import pygame
import random

pygame.init()

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

class Board:
    def __init__(self, rows, cols, difficulty='easy'):
        self.rows = rows
        self.cols = cols
        self.board = self.generate_board(difficulty)
        self.original_board = [row[:] for row in self.board]
        self.cell_size = 600 // rows
        self.selected_cell = None

    def generate_board(self, difficulty):
        def is_valid(board, row, col, num):
            for i in range(9):
                if board[row][i] == num or board[i][col] == num:
                    return False
            start_row, start_col = 3 * (row // 3), 3 * (col // 3)
            for i in range(3):
                for j in range(3):
                    if board[start_row + i][start_col + j] == num:
                        return False
            return True

        def solve(board):
            for row in range(9):
                for col in range(9):
                    if board[row][col] == 0:
                        for num in range(1, 10):
                            if is_valid(board, row, col, num):
                                board[row][col] = num
                                if solve(board):
                                    return True
                                board[row][col] = 0
                        return False
            return True

        board = [[0] * 9 for _ in range(9)]
        solve(board)
        empty_spots = {'easy': 30, 'medium': 40, 'hard': 50}
        spots = random.sample(range(81), empty_spots[difficulty])
        for spot in spots:
            board[spot // 9][spot % 9] = 0
        return board

    def draw(self, screen):
        for i in range(self.rows + 1):
            line_width = 3 if i % 3 == 0 else 1
            pygame.draw.line(screen, (0, 0, 0), (0, i * self.cell_size), (600, i * self.cell_size), line_width)
            pygame.draw.line(screen, (0, 0, 0), (i * self.cell_size, 0), (i * self.cell_size, 600), line_width)

        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    self.draw_number(screen, self.board[i][j], i, j)

        if self.selected_cell:
            self.highlight_selected_cell(screen)

    def draw_number(self, screen, number, row, col):
        font = pygame.font.Font(None, 60)
        text = font.render(str(number), True, (0, 0, 0))
        screen.blit(text, (col * self.cell_size + 20, row * self.cell_size + 10))

    def highlight_selected_cell(self, screen):
        pygame.draw.rect(screen, (0, 255, 0),
                         (self.selected_cell[1] * self.cell_size, self.selected_cell[0] * self.cell_size,
                          self.cell_size, self.cell_size), 3)

    def click(self, x, y):
        if x < 600 and y < 600:
            row = y // self.cell_size
            col = x // self.cell_size
            return row, col
        return None

    def select(self, row, col):
        self.selected_cell = (row, col)

    def sketch(self, number):
        if self.selected_cell:
            row, col = self.selected_cell
            self.board[row][col] = int(number)

    def place_number(self, number):
        if self.selected_cell:
            row, col = self.selected_cell
            self.board[row][col] = int(number)

    def reset_to_original(self):
        self.board = [row[:] for row in self.original_board]

    def is_full(self):
        for row in self.board:
            if 0 in row:
                return False
        return True

    def valid_board(self):
        for row in range(self.rows):
            if not self.valid_row(row):
                return False
        for col in range(self.cols):
            if not self.valid_col(col):
                return False
        for row in range(0, self.rows, 3):
            for col in range(0, self.cols, 3):
                if not self.valid_box(row, col):
                    return False
        return True

    def valid_row(self, row):
        row_values = [num for num in self.board[row] if num != 0]
        return len(row_values) == len(set(row_values))

    def valid_col(self, col):
        col_values = [self.board[row][col] for row in range(self.rows) if self.board[row][col] != 0]
        return len(col_values) == len(set(col_values))

    def valid_box(self, start_row, start_col):
        box_values = []
        for i in range(3):
            for j in range(3):
                if self.board[start_row + i][start_col + j] != 0:
                    box_values.append(self.board[start_row + i][start_col + j])
        return len(box_values) == len(set(box_values))

def draw_start_screen(screen):
    font = pygame.font.Font(None, 100)
    text = font.render("Sudoku", True, (0, 0, 0))
    screen.blit(text, (150, 250))

    font = pygame.font.Font(None, 50)
    text = font.render("Press any key to start", True, (0, 0, 0))
    screen.blit(text, (130, 350))

def draw_game_over_screen(screen):
    font = pygame.font.Font(None, 100)
    text = font.render("Game Over", True, (255, 0, 0))
    screen.blit(text, (100, 250))

    font = pygame.font.Font(None, 50)
    text = font.render("Press ESC to restart", True, (0, 0, 0))
    screen.blit(text, (130, 350))

def main():
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Sudoku")

    game_start_state = True
    game_over = False
    board = None

    while True:
        screen.fill((255, 255, 255))

        if game_start_state:
            button_rect_1, button_rect_2, button_rect_3 = game_start(screen)
        elif game_over:
            draw_game_over_screen(screen)
        else:
            board.draw(screen)
            if board.is_full() and board.valid_board():
                game_over = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_start_state:
                    mouse_pos = event.pos
                    if button_rect_1.collidepoint(mouse_pos):
                        board = Board(9, 9, 'easy')
                        game_start_state = False
                    elif button_rect_2.collidepoint(mouse_pos):
                        board = Board(9, 9, 'medium')
                        game_start_state = False
                    elif button_rect_3.collidepoint(mouse_pos):
                        board = Board(9, 9, 'hard')
                        game_start_state = False
                elif not game_over:
                    pos = pygame.mouse.get_pos()
                    clicked = board.click(pos[0], pos[1])
                    if clicked:
                        board.select(clicked[0], clicked[1])
            elif event.type == pygame.KEYDOWN:
                if game_start_state:
                    game_start_state = False
                elif not game_start_state and not game_over:
                    if chr(event.key).isdigit() and chr(event.key) != "0":
                        board.sketch(chr(event.key))
                    elif event.key == pygame.K_RETURN:
                        if board.selected_cell:
                            board.place_number(board.board[board.selected_cell[0]][board.selected_cell[1]])
                    elif event.key == pygame.K_r:
                        board.reset_to_original()
                    elif event.key == pygame.K_ESCAPE:
                        game_start_state = True
                        game_over = False

        pygame.display.flip()

if __name__ == "__main__":
    main()

