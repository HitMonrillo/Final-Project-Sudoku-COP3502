import pygame
import random
import math
import sys
from sudoku_generator import SudokuGenerator

pygame.init()
gator_img = pygame.image.load("8bit-gator.png")
scaled_img = pygame.transform.scale(gator_img, (200, 200))


def draw_button(surface, color, rect, text, text_color, font):
    pygame.draw.rect(surface, color, rect, border_radius=10)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)


def create_surface(surface, text, font, color, center):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=center)
    surface.blit(text_surface, text_rect)


def game_start(screen):
    pygame.init()

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (30, 144, 255)
    DARK_BLUE = (0, 0, 139)
    BUTTON_COLOR = (255, 69, 0)
    BUTTON_HOVER_COLOR = (255, 140, 0)
    WIDTH = 800
    HEIGHT = 800
    BUTTON_WIDTH = 150
    BUTTON_HEIGHT = 60

    start_title_font = pygame.font.Font(None, 100)
    game_mode_font = pygame.font.Font(None, 60)
    button_font = pygame.font.Font(None, 40)

    screen.fill(WHITE)

    create_surface(
        screen,
        "Welcome To Sudoku",
        start_title_font,
        DARK_BLUE,
        (WIDTH // 2, HEIGHT // 3 - 100),
    )
    create_surface(
        screen,
        "Select Game Mode:",
        game_mode_font,
        BLUE,
        (WIDTH // 2, HEIGHT // 2 - 100),
    )

    button_rect_1 = pygame.Rect(
        WIDTH // 4 - BUTTON_WIDTH // 2, HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT
    )
    button_rect_2 = pygame.Rect(
        WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT
    )
    button_rect_3 = pygame.Rect(
        3 * WIDTH // 4 - BUTTON_WIDTH // 2, HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT
    )

    draw_button(screen, BUTTON_COLOR, button_rect_1, "Easy", WHITE, button_font)
    draw_button(screen, BUTTON_COLOR, button_rect_2, "Medium", WHITE, button_font)
    draw_button(screen, BUTTON_COLOR, button_rect_3, "Hard", WHITE, button_font)

    # Load and scale an image if needed (ensure 'scaled_img' is defined and loaded elsewhere in your code)
    screen.blit(scaled_img, (300, 500))

    return button_rect_1, button_rect_2, button_rect_3


def generate_sudoku(size, removed):
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    board = sudoku.get_board()
    sudoku.remove_cells()
    return board


class Board:
    def __init__(self, rows, cols, difficulty="easy"):
        self.rows = rows
        self.cols = cols
        self.cell_size = 600 // rows
        self.board = generate_sudoku(rows, self.get_removed_cells(difficulty))
        self.fixed_board = [
            [cell if cell != 0 else None for cell in row] for row in self.board
        ]
        self.board_backup = [row[:] for row in self.board]
        self.fixed_board_backup = [row[:] for row in self.fixed_board]
        self.selected_cell = None
        self.buttons = {
            "reset": pygame.Rect(650, 50, 120, 50),
            "restart": pygame.Rect(650, 120, 120, 50),
            "exit": pygame.Rect(650, 190, 120, 50),
        }

    def draw_buttons(self, screen):
        button_font = pygame.font.Font(None, 35)
        BUTTON_COLOR = (255, 69, 0)

        draw_button(
            screen,
            (255, 69, 0),
            self.buttons["reset"],
            "Reset",
            (255, 255, 255),
            button_font,
        )
        draw_button(
            screen,
            (255, 69, 0),
            self.buttons["restart"],
            "Restart",
            (255, 255, 255),
            button_font,
        )
        draw_button(
            screen,
            (255, 69, 0),
            self.buttons["exit"],
            "Exit",
            (255, 255, 255),
            button_font,
        )

    def get_removed_cells(self, difficulty):
        if difficulty == "easy":
            return 30
        elif difficulty == "medium":
            return 40
        elif difficulty == "hard":
            return 50
        return 30

    def draw(self, screen):
        for i in range(self.rows + 1):
            line_width = 3 if i % 3 == 0 else 1
            pygame.draw.line(
                screen,
                (0, 0, 0),
                (0, i * self.cell_size),
                (600, i * self.cell_size),
                line_width,
            )
            pygame.draw.line(
                screen,
                (0, 0, 0),
                (i * self.cell_size, 0),
                (i * self.cell_size, 600),
                line_width,
            )

        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0 or self.fixed_board[i][j] is not None:
                    self.draw_number(
                        screen,
                        (
                            self.board[i][j]
                            if self.board[i][j] != 0
                            else self.fixed_board[i][j]
                        ),
                        i,
                        j,
                        self.fixed_board[i][j] is not None,
                    )

        if self.selected_cell:
            self.highlight_selected_cell(screen)

        self.draw_buttons(screen)

    def handle_button_click(self, pos, screen):
        if self.buttons["reset"].collidepoint(pos):
            self.reset_to_original(screen)
        elif self.buttons["restart"].collidepoint(pos):
            self.restart_game(screen)
            return True
        elif self.buttons["exit"].collidepoint(pos):
            pygame.quit()
            sys.exit()

    def draw_number(self, screen, number, row, col, fixed):
        font = pygame.font.Font(None, 60)
        color = (0, 0, 0) if fixed else (0, 0, 255)
        text = font.render(str(number), True, color)
        screen.blit(text, (col * self.cell_size + 20, row * self.cell_size + 10))

    def highlight_selected_cell(self, screen):
        pygame.draw.rect(
            screen,
            (0, 255, 0),
            (
                self.selected_cell[1] * self.cell_size,
                self.selected_cell[0] * self.cell_size,
                self.cell_size,
                self.cell_size,
            ),
            3,
        )

    def restart_game(self, screen):
        # Restart the game with the same difficulty level
        self.board = generate_sudoku(self.rows, self.get_removed_cells("easy"))
        self.fixed_board = [
            [cell if cell != 0 else None for cell in row] for row in self.board
        ]
        self.selected_cell = None
        game_start(screen)
        return True

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
            if self.fixed_board[row][col] is None:
                self.board[row][col] = int(number)

    def place_number(self, number):
        if self.selected_cell:
            row, col = self.selected_cell
            if self.fixed_board[row][col] is None:
                self.board[row][col] = int(number)

    def reset_to_original(self, screen):
        self.board = [row[:] for row in self.board_backup]
        self.fixed_board = [row[:] for row in self.fixed_board_backup]
        self.selected_cell = None

        screen.fill((255, 255, 255))

        self.draw(screen)

        # Update the display
        pygame.display.update()

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
        nums = set()
        for num in self.board[row]:
            if num != 0:
                if num in nums:
                    return False
                nums.add(num)
        return True

    def valid_col(self, col):
        nums = set()
        for row in range(self.rows):
            num = self.board[row][col]
            if num != 0:
                if num in nums:
                    return False
                nums.add(num)
        return True

    def valid_box(self, start_row, start_col):
        nums = set()
        for row in range(start_row, start_row + 3):
            for col in range(start_col, start_col + 3):
                num = self.board[row][col]
                if num != 0:
                    if num in nums:
                        return False
                    nums.add(num)
        return True

    def move_selection(self, direction):
        if self.selected_cell:
            row, col = self.selected_cell
            if direction == "UP" and row > 0:
                row -= 1
            elif direction == "DOWN" and row < self.rows - 1:
                row += 1
            elif direction == "LEFT" and col > 0:
                col -= 1
            elif direction == "RIGHT" and col < self.cols - 1:
                col += 1
            self.selected_cell = (row, col)
        else:
            self.selected_cell = (0, 0)

    def move_arrow(self, direction):
        if self.selected_cell:
            row, col = self.selected_cell
            if direction == "UP" and row > 0:
                row -= 1
            elif direction == "DOWN" and row < self.rows - 1:
                row += 1
            elif direction == "LEFT" and col > 0:
                col -= 1
            elif direction == "RIGHT" and col < self.cols - 1:
                col += 1
            self.selected_cell = (row, col)
        else:
            self.selected_cell = (0, 0)


def draw_start_screen(screen):
    font = pygame.font.Font(None, 100)
    text = font.render("Sudoku", True, (0, 0, 0))
    screen.blit(text, (150, 250))

    font = pygame.font.Font(None, 50)
    text = font.render("Press any key to start", True, (0, 0, 0))
    screen.blit(text, (130, 350))


def draw_game_over_screen(screen, game_won):
    font = pygame.font.Font(None, 100)
    text_color = (255, 69, 0) if not game_won else (30, 144, 255)
    text = font.render("Game Over" if not game_won else "You Win!", True, text_color)
    screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 250))

    button_font = pygame.font.Font(None, 50)
    restart_text = button_font.render("Restart", True, (255, 255, 255))
    exit_text = button_font.render("Exit", True, (255, 255, 255))

    button_color = (255, 69, 0)
    button_hover_color = (255, 140, 0)
    button_width = 200
    button_height = 60
    button_y_start = 400

    if not game_won:
        restart_button_rect = pygame.Rect(
            screen.get_width() // 2 - button_width // 2,
            button_y_start,
            button_width,
            button_height,
        )
        pygame.draw.rect(screen, button_color, restart_button_rect, border_radius=10)
        screen.blit(
            restart_text,
            (
                restart_button_rect.centerx - restart_text.get_width() // 2,
                restart_button_rect.centery - restart_text.get_height() // 2,
            ),
        )

    exit_button_rect = pygame.Rect(
        screen.get_width() // 2 - button_width // 2,
        button_y_start + 70,
        button_width,
        button_height,
    )
    pygame.draw.rect(screen, button_color, exit_button_rect, border_radius=10)
    screen.blit(
        exit_text,
        (
            exit_button_rect.centerx - exit_text.get_width() // 2,
            exit_button_rect.centery - exit_text.get_height() // 2,
        ),
    )


def main():
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Sudoku")

    game_start_state = True
    game_over = False
    game_won = False
    board = None

    while True:
        screen.fill((255, 255, 255))

        if game_start_state:
            button_rect_1, button_rect_2, button_rect_3 = game_start(screen)
        elif game_over:
            draw_game_over_screen(screen, game_won)
        else:
            board.draw(screen)
            if board.is_full():
                if board.valid_board():
                    game_won = True
                else:
                    game_won = False
                game_over = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_start_state:
                    mouse_pos = event.pos
                    if button_rect_1.collidepoint(mouse_pos):
                        board = Board(9, 9, "easy")
                        game_start_state = False
                    elif button_rect_2.collidepoint(mouse_pos):
                        board = Board(9, 9, "medium")
                        game_start_state = False
                    elif button_rect_3.collidepoint(mouse_pos):
                        board = Board(9, 9, "hard")
                        game_start_state = False
                elif game_over:
                    mouse_pos = event.pos
                    if pygame.Rect(300, 470, 200, 50).collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
                    elif pygame.Rect(300, 400, 200, 50).collidepoint(mouse_pos):
                        game_over = False
                        game_start_state = True
                        board = None
                elif not game_over:
                    mouse_pos = event.pos
                    if board.click(mouse_pos[0], mouse_pos[1]) is not None:
                        row, col = board.click(mouse_pos[0], mouse_pos[1])
                        board.select(row, col)
                        board.draw(screen)
                    else:
                        if board.handle_button_click(mouse_pos, screen):
                            screen = pygame.display.set_mode((800, 800))
                            pygame.display.set_caption("Sudoku")
                            game_start_state = True
                            game_over = False
                            game_won = False
                            board = None

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if game_over:
                        game_start_state = True
                        game_over = False
                        board = None
                    else:
                        game_start_state = True
                        game_over = False
                        board = None
                elif event.key == pygame.K_UP:
                    board.move_arrow("UP")
                elif event.key == pygame.K_DOWN:
                    board.move_arrow("DOWN")
                elif event.key == pygame.K_LEFT:
                    board.move_arrow("LEFT")
                elif event.key == pygame.K_RIGHT:
                    board.move_arrow("RIGHT")
                elif event.key in (
                    pygame.K_1,
                    pygame.K_2,
                    pygame.K_3,
                    pygame.K_4,
                    pygame.K_5,
                    pygame.K_6,
                    pygame.K_7,
                    pygame.K_8,
                    pygame.K_9,
                ):
                    board.sketch(event.key - pygame.K_0)
                elif event.key == pygame.K_RETURN:
                    board.place_number(
                        board.board[board.selected_cell[0]][board.selected_cell[1]]
                        if board.selected_cell
                        else 0
                    )
                    board.sketch(event.key - pygame.K_0)
                elif event.key == pygame.K_RETURN:
                    board.place_number(
                        board.board[board.selected_cell[0]][board.selected_cell[1]]
                        if board.selected_cell
                        else 0
                    )

        pygame.display.flip()


if __name__ == "__main__":
    main()
