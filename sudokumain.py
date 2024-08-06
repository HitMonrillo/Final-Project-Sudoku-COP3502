import pygame
import random
import math
import sys
from sudoku_generator import SudokuGenerator

pygame.init()


# Function for drawing the button for opening menu screen
def draw_button(surface, color, rect, text, text_color, font):
    pygame.draw.rect(surface, color, rect, border_radius=10)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)


# Function for creating teh surface for opening menu screen
def create_surface(surface, text, font, color, center):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=center)
    surface.blit(text_surface, text_rect)


# Function that delivers the opening menu screen visuals on game start
def game_start(screen):
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
        (WIDTH // 2, HEIGHT // 3 - 150),
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
    gator_img = pygame.image.load("8bit-gator.png")
    scaled_img = pygame.transform.scale(gator_img, (200, 200))
    screen.blit(scaled_img, (300, 500))

    return button_rect_1, button_rect_2, button_rect_3


# Function that generates sudoku board from SudokuGenerator Class
def generate_sudoku(size, removed):
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    board = sudoku.get_board()
    sudoku.remove_cells()
    return board


# Class Board Constructor
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
        self.entered_numbers = [[False for col in range(cols)] for row in range(rows)]

    # Draw buttons for the board
    def draw_buttons(self, screen):
        button_font = pygame.font.Font(None, 35)

        button_color = (255, 69, 0)
        button_text_color = (255, 255, 255)

        draw_button(
            screen,
            button_color,
            self.buttons["reset"],
            "Reset",
            button_text_color,
            button_font,
        )
        draw_button(
            screen,
            button_color,
            self.buttons["restart"],
            "Restart",
            button_text_color,
            button_font,
        )
        draw_button(
            screen,
            button_color,
            self.buttons["exit"],
            "Exit",
            button_text_color,
            button_font,
        )

    # Deliver removed num of cells
    def get_removed_cells(self, difficulty):
        if difficulty == "easy":
            return 30
        elif difficulty == "medium":
            return 40
        elif difficulty == "hard":
            return 50
        return 30

    # Draw the Sudoku board
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

    # Logic for handling in-game buttons - reset, restart, and exit
    def handle_button_click(self, pos, screen):
        if self.buttons["reset"].collidepoint(pos):
            self.reset_to_original(screen)
        elif self.buttons["restart"].collidepoint(pos):
            self.restart_game(screen)
            return True
        elif self.buttons["exit"].collidepoint(pos):
            pygame.quit()
            sys.exit()

    # Logic for accepting number input from user
    def draw_number(self, screen, number, row, col, fixed):
        font = pygame.font.Font(None, 60)
        if fixed:
            color = (0, 0, 0)
        elif self.entered_numbers[row][col]:
            color = (0, 0, 139)  # Dark blue
        else:
            color = (30, 144, 255)  # Light blue
        text = font.render(str(number), True, color)
        screen.blit(text, (col * self.cell_size + 20, row * self.cell_size + 10))

    # Enters the number as dark blue when clicking return
    def enter_number(self, screen, row, col):
        if self.selected_cell:
            row, col = self.selected_cell
            number = self.board[row][col]
            if number == 0:
                return False
            self.entered_numbers[row][col] = True
            return True
        return False

    # Highlights the cell to create UI showing which cell the user is entering into
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

    # Logic for restarting the game
    def restart_game(self, screen):

        game_start(screen)
        return True

    # Captures relevant click information. Returns none if outside bound of Sudoku board, meaning it was one of the buttons
    def click(self, x, y):
        if x < 600 and y < 600:
            row = y // self.cell_size
            col = x // self.cell_size
            return row, col
        return None

    # Sets the selected cell
    def select(self, row, col):
        self.selected_cell = (row, col)

    # Adds number to the cell
    def sketch(self, number):
        if self.selected_cell:
            row, col = self.selected_cell
            if self.fixed_board[row][col] is None:
                if self.board[row][col] != int(number):
                    self.entered_numbers[row][col] = False
                self.board[row][col] = int(number)

    # Places the users number in
    def place_number(self, number):
        if self.selected_cell:
            row, col = self.selected_cell
            if self.fixed_board[row][col] is None:
                self.board[row][col] = int(number)

    # Logic for resetting the board, removing current numbers. Utilizing deep copy method
    def reset_to_original(self, screen):
        self.board = [row[:] for row in self.board_backup]
        self.fixed_board = [row[:] for row in self.fixed_board_backup]
        self.selected_cell = None

        screen.fill((255, 255, 255))

        self.draw(screen)

        # Update the display
        pygame.display.update()

    # Check if all numbers entered are selected + dark blue
    def all_numbers_entered(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if (
                    self.board[i][j] != 0
                    and not self.entered_numbers[i][j]
                    and self.fixed_board[i][j] is None
                ):
                    return False
        return True

    # Checks if board is full
    def is_full(self):
        for row in self.board:
            if 0 in row:
                return False
        return True

    # Check if board is valid
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

    #  Captures arrow movement between each cell
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


# Draws the game when game mode is entered
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


# Main function instantiating the game logic
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
            if board.is_full() and board.all_numbers_entered():
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
                    if board.enter_number(screen, row, col):
                        pygame.display.flip()

        pygame.display.flip()


if __name__ == "__main__":
    main()
