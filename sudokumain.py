import pygame
import random
import math
import sys
from sudoku_generator import SudokuGenerator

# Initialize Pygame
pygame.init()

# Load and scale an image to be used in the game
gator_img = pygame.image.load("8bit-gator.png")
scaled_img = pygame.transform.scale(gator_img, (200, 200))


# Function to draw a button with text on a Pygame surface
def draw_button(surface, color, rect, text, text_color, font):
    pygame.draw.rect(surface, color, rect, border_radius=10)  # Draw button rectangle
    text_surface = font.render(text, True, text_color)  # Render the button text
    text_rect = text_surface.get_rect(
        center=rect.center
    )  # Center the text on the button
    surface.blit(text_surface, text_rect)  # Draw the text on the surface


# Function to create a text surface and blit it onto a Pygame surface
def create_surface(surface, text, font, color, center):
    text_surface = font.render(text, True, color)  # Render the text
    text_rect = text_surface.get_rect(center=center)  # Center the text
    surface.blit(text_surface, text_rect)  # Draw the text on the surface


# Function to initialize and display the game start screen
def game_start(screen):
    pygame.init()  # Initialize Pygame

    # Define colors
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

    # Define fonts
    start_title_font = pygame.font.Font(None, 100)
    game_mode_font = pygame.font.Font(None, 60)
    button_font = pygame.font.Font(None, 40)

    # Fill the screen with white color
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

    # Load and scale an image if needed (ensure 'scaled_img' is defined and loaded elsewhere in your code)
    screen.blit(scaled_img, (300, 500))

    return button_rect_1, button_rect_2, button_rect_3


# Function to generate a Sudoku board of a given size with a specified number of cells removed
def generate_sudoku(size, removed):
    sudoku = SudokuGenerator(size, removed)  # Create a new Sudoku generator
    sudoku.fill_values()  # Fill the Sudoku board with values
    board = sudoku.get_board()  # Get the filled Sudoku board
    sudoku.remove_cells()  # Remove cells to create the puzzle
    return board


# Class to represent the Sudoku board and its functionality
class Board:
    def __init__(self, rows, cols, difficulty="easy"):
        self.rows = rows
        self.cols = cols
        self.cell_size = 600 // rows  # Calculate cell size based on the board size
        self.board = generate_sudoku(
            rows, self.get_removed_cells(difficulty)
        )  # Generate the initial board
        self.fixed_board = [
            [cell if cell != 0 else None for cell in row] for row in self.board
        ]  # Create the fixed board
        self.board_backup = [row[:] for row in self.board]  # Backup the initial board
        self.fixed_board_backup = [
            row[:] for row in self.fixed_board
        ]  # Backup the fixed board
        self.selected_cell = None  # No cell is selected initially
        self.buttons = {  # Define button positions and sizes
            "reset": pygame.Rect(650, 50, 120, 50),
            "restart": pygame.Rect(650, 120, 120, 50),
            "exit": pygame.Rect(650, 190, 120, 50),
        }

    # Function to draw buttons on the screen
    def draw_buttons(self, screen):
        button_font = pygame.font.Font(None, 35)
        draw_button(
            screen, (255, 0, 0), self.buttons["reset"], "Reset", (0, 0, 0), button_font
        )
        draw_button(
            screen,
            (255, 0, 0),
            self.buttons["restart"],
            "Restart",
            (0, 0, 0),
            button_font,
        )
        draw_button(
            screen, (255, 0, 0), self.buttons["exit"], "Exit", (0, 0, 0), button_font
        )

    def get_removed_cells(self, difficulty):
        if difficulty == "easy":
            return 30
        elif difficulty == "medium":
            return 40
        elif difficulty == "hard":
            return 50
        return 30

    # Function to draw the Sudoku board and its elements on the screen
    def draw(self, screen):
        for i in range(self.rows + 1):
            line_width = 3 if i % 3 == 0 else 1  # Set line width for grid lines
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

    # Function to handle button clicks and perform corresponding actions
    def handle_button_click(self, pos, screen):
        if self.buttons["reset"].collidepoint(pos):
            self.reset_to_original(screen)
        elif self.buttons["restart"].collidepoint(pos):
            self.restart_game(screen)
            return True
        elif self.buttons["exit"].collidepoint(pos):
            pygame.quit()
            sys.exit()

    # Function to draw a number in a cell on the screen
    def draw_number(self, screen, number, row, col, fixed):
        font = pygame.font.Font(None, 60)
        color = (0, 0, 0) if fixed else (0, 0, 255)
        text = font.render(str(number), True, color)
        screen.blit(text, (col * self.cell_size + 20, row * self.cell_size + 10))

    # Function to highlight the selected cell on the screen
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

    # Function to restart the game with the same difficulty level
    def restart_game(self, screen):
        # Restart the game with the same difficulty level
        # self.board = generate_sudoku(self.rows, self.get_removed_cells("easy"))
        # self.fixed_board = [
        #     [cell if cell != 0 else None for cell in row] for row in self.board
        # ]
        # self.selected_cell = None
        game_start(screen)
        return True

    # Function to handle mouse clicks on the Sudoku board
    def click(self, x, y):
        if x < 600 and y < 600:
            row = y // self.cell_size
            col = x // self.cell_size
            return row, col
        return None

    # Function to select a cell on the Sudoku board
    def select(self, row, col):
        self.selected_cell = (row, col)

    # Function to sketch a number in the selected cell
    def sketch(self, number):
        if self.selected_cell:
            row, col = self.selected_cell
            if self.fixed_board[row][col] is None:
                self.board[row][col] = number

    # Function to reset the Sudoku board to its original state
    def reset_to_original(self, screen):
        self.board = [row[:] for row in self.board_backup]
        self.fixed_board = [row[:] for row in self.fixed_board_backup]
        self.draw(screen)
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
    pygame.init()
    screen = pygame.display.set_mode((800, 800))  # Set screen size
    pygame.display.set_caption("Sudoku")  # Set window title
    clock = pygame.time.Clock()
    running = True
    game_start(screen)

    button_rect_1, button_rect_2, button_rect_3 = game_start(screen)
    board = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not board:
                    if button_rect_1.collidepoint(event.pos):
                        board = Board(9, 9, "easy")
                    elif button_rect_2.collidepoint(event.pos):
                        board = Board(9, 9, "medium")
                    elif button_rect_3.collidepoint(event.pos):
                        board = Board(9, 9, "hard")
                    if board:
                        screen.fill((255, 255, 255))
                        board.draw(screen)
                else:
                    pos = pygame.mouse.get_pos()
                    cell = board.click(pos[0], pos[1])
                    if cell:
                        board.select(cell[0], cell[1])
                    else:
                        board.handle_button_click(pos, screen)

            elif event.type == pygame.KEYDOWN and board:
                if event.key == pygame.K_1:
                    board.sketch(1)
                elif event.key == pygame.K_2:
                    board.sketch(2)
                elif event.key == pygame.K_3:
                    board.sketch(3)
                elif event.key == pygame.K_4:
                    board.sketch(4)
                elif event.key == pygame.K_5:
                    board.sketch(5)
                elif event.key == pygame.K_6:
                    board.sketch(6)
                elif event.key == pygame.K_7:
                    board.sketch(7)
                elif event.key == pygame.K_8:
                    board.sketch(8)
                elif event.key == pygame.K_9:
                    board.sketch(9)

        if board:
            screen.fill((255, 255, 255))
            board.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


# Call the main function to start the game
if __name__ == "__main__":
    main()
