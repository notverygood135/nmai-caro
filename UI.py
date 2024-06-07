import pygame
from game import Game

# Initialize Pygame
pygame.init()

# Constants for colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
LIGHT_GRAY = (220, 220, 220)  # Define LIGHT_GRAY color
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Constants for the window size and square size
WINDOW_SIZE = 450
SQUARE_SIZE = WINDOW_SIZE // 3

# Button constants
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50
BUTTON_COLOR = GRAY
BUTTON_HOVER_COLOR = LIGHT_GRAY
BUTTON_TEXT_COLOR = BLACK
BUTTON_TEXT_HOVER_COLOR = BLACK

# Initialize the game outside of the main function scope
game = Game(3)
gamecode = None
screen = pygame.display.set_mode(
    (WINDOW_SIZE, WINDOW_SIZE + BUTTON_HEIGHT + BUTTON_HEIGHT + BUTTON_HEIGHT))  # Adjusted window height
pygame.display.set_caption("Tic-Tac-Toe")

# Font for displaying text
font = pygame.font.Font(None, 40)
button_font = pygame.font.Font(None, 30)


# Function to draw the game board
def draw_board(screen, button_font):
    screen.fill(WHITE)
    # Draw horizontal lines
    for i in range(1, 3):
        pygame.draw.line(screen, BLACK, (0, i * SQUARE_SIZE), (WINDOW_SIZE, i * SQUARE_SIZE), 2)
    # Draw vertical lines
    for i in range(1, 3):
        pygame.draw.line(screen, BLACK, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, WINDOW_SIZE), 2)

    # Draw Restart button
    restart_button_rect = draw_button(screen, WINDOW_SIZE // 3 - BUTTON_WIDTH // 2, WINDOW_SIZE + BUTTON_HEIGHT,
                                      BUTTON_WIDTH, BUTTON_HEIGHT, "Restart", button_font, BUTTON_TEXT_COLOR,
                                      BUTTON_COLOR)

    # Draw Quit button
    quit_button_rect = draw_button(screen, WINDOW_SIZE // 3 + WINDOW_SIZE // 3 - BUTTON_WIDTH // 2,
                                   WINDOW_SIZE + BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT, "Quit", button_font,
                                   BUTTON_TEXT_COLOR, BUTTON_COLOR)

    # Write type of current AI (if play vs AI)
    if gamecode == 3:
        display_text(screen, "AI mode: Minimax Algorithm", button_font, BLUE, WINDOW_SIZE // 2,
                     WINDOW_SIZE + BUTTON_HEIGHT * 2 + 25)
    elif gamecode == 4:
        display_text(screen, "AI mode: Alpha-Beta Algorithm", button_font, BLUE, WINDOW_SIZE // 2,
                     WINDOW_SIZE + BUTTON_HEIGHT * 2 + 25)
    elif gamecode == 5:
        display_text(screen, "AI mode: MCTS Algorithm", button_font, BLUE, WINDOW_SIZE // 2,
                     WINDOW_SIZE + BUTTON_HEIGHT * 2 + 25)
    return restart_button_rect, quit_button_rect


# Function to draw X's and O's on the board
def draw_moves(screen):
    for row in range(3):
        for col in range(3):
            if game.board[row][col] == 'x':
                pygame.draw.line(screen, RED, (col * SQUARE_SIZE + 10, row * SQUARE_SIZE + 10),
                                 ((col + 1) * SQUARE_SIZE - 10, (row + 1) * SQUARE_SIZE - 10), 4)
                pygame.draw.line(screen, RED, ((col + 1) * SQUARE_SIZE - 10, row * SQUARE_SIZE + 10),
                                 (col * SQUARE_SIZE + 10, (row + 1) * SQUARE_SIZE - 10), 4)
            elif game.board[row][col] == 'o':
                pygame.draw.circle(screen, BLUE,
                                   (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   SQUARE_SIZE // 2 - 10, 4)


# Function to display text on the screen with space
def display_text(screen, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)


# Function to create buttons
def draw_button(screen, x, y, width, height, text, font, text_color, bg_color):
    pygame.draw.rect(screen, bg_color, (x, y, width, height),width=1,border_radius=15)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
    
    screen.blit(text_surface, text_rect)
    return text_rect  # Return button rectangle


def draw_menu(screen, button_font):
    menu_running = True
    global gamecode

    while menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Check if the play button is clicked
                if play_button_rect.collidepoint(mouse_pos):
                    gamecode = 1
                    menu_running = False  # Exit the menu loop
                # Check if the quit button is clicked
                elif play_button_AI_rect2.collidepoint(mouse_pos):
                    draw_ai_menu(screen, button_font)
                    menu_running = False  # Exit the menu loop
                elif quit_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
        # Draw menu buttons
        screen.fill(WHITE)
        # Draw the play button and get its rectangle
        play_button_rect = draw_button(screen, WINDOW_SIZE // 2 - BUTTON_WIDTH - 10,
                                       WINDOW_SIZE // 2 - BUTTON_HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT, "1vs1",
                                       button_font, BUTTON_TEXT_COLOR, BUTTON_COLOR)
        play_button_AI_rect2 = draw_button(screen, WINDOW_SIZE // 2 + 10, WINDOW_SIZE // 2 - BUTTON_HEIGHT // 2,
                                           BUTTON_WIDTH, BUTTON_HEIGHT, "Vs AI", button_font, BUTTON_TEXT_COLOR,
                                           BUTTON_COLOR)

        # Draw the quit button and get its rectangle
        quit_button_rect = draw_button(screen, WINDOW_SIZE // 2 - BUTTON_WIDTH // 2, WINDOW_SIZE // 2 + BUTTON_HEIGHT,
                                       BUTTON_WIDTH, BUTTON_HEIGHT, "Quit", button_font, BUTTON_TEXT_COLOR,
                                       BUTTON_COLOR)

        display_text(screen, "MENU", font, BLUE, WINDOW_SIZE // 2, WINDOW_SIZE // 3)
        pygame.display.flip()


# Function to draw AI menu screen
def draw_ai_menu(screen, button_font):
    menu_running = True
    global gamecode
    while menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Check if the play button is clicked
                if minimax_button_rect.collidepoint(mouse_pos):
                    gamecode = 3
                    menu_running = False  # Exit the menu loop
                elif alpha_beta_button_rect.collidepoint(mouse_pos):
                    gamecode = 4
                    menu_running = False  # Exit the menu loop
                elif mcts_button_rect.collidepoint(mouse_pos):
                    gamecode = 5
                    menu_running = False  # Exit the menu loop
                elif back_button_rect.collidepoint(mouse_pos):
                    menu_running = False  # Exit the menu loop
                    draw_menu(screen, button_font)
        screen.fill(WHITE)
        # Draw the play button and get its rectangle
        display_text(screen, "CHOOSE AI MODE", button_font, BLUE, WINDOW_SIZE // 2, WINDOW_SIZE // 4)
        minimax_button_rect = draw_button(screen, WINDOW_SIZE // 2 - BUTTON_WIDTH // 2,
                                          WINDOW_SIZE // 2 - BUTTON_HEIGHT // 2, BUTTON_WIDTH+15, BUTTON_HEIGHT, "Minimax",
                                          button_font, BUTTON_TEXT_COLOR, BUTTON_COLOR)
        alpha_beta_button_rect = draw_button(screen, WINDOW_SIZE // 2 - BUTTON_WIDTH // 2,
                                             WINDOW_SIZE // 2 + BUTTON_HEIGHT, BUTTON_WIDTH+15, BUTTON_HEIGHT,
                                             "Alpha-Beta", button_font, BUTTON_TEXT_COLOR, BUTTON_COLOR)
        mcts_button_rect = draw_button(screen, WINDOW_SIZE // 2 - BUTTON_WIDTH // 2,
                                       WINDOW_SIZE // 2 + BUTTON_HEIGHT * 2 + BUTTON_HEIGHT // 2, BUTTON_WIDTH+15,
                                       BUTTON_HEIGHT, "MCTS", button_font, BUTTON_TEXT_COLOR, BUTTON_COLOR)
        back_button_rect = draw_button(screen, 0, 0, BUTTON_WIDTH, BUTTON_HEIGHT, "Back", button_font,
                                       BUTTON_TEXT_COLOR, BUTTON_COLOR)
        pygame.display.flip()


# Function to handle restart button click
def handle_restart_button_click():
    global game
    game = Game(3)  # Restart the game
    draw_board(screen, button_font)
    draw_moves(screen)
    print("Game restarted")
    pygame.display.flip()


# Function to handle quit button click
def handle_quit_button_click():
    global game
    game = Game(3)  # Restart the game

# Function to play 1vs1
def play_1vs1():
            running = True
            restart_button_rect, quit_button_rect = draw_board(screen, button_font)
            while running:
                # Draw the game board
                draw_board(screen, button_font)
                # Draw X's and O's
                draw_moves(screen)
                # Display "Make your move!"
                if game.player_turn == 1:
                    display_text(screen, "X's turn", font, BLACK, WINDOW_SIZE // 2, WINDOW_SIZE + 20)
                elif game.player_turn == 2:
                    display_text(screen, "O's turn", font, BLACK, WINDOW_SIZE // 2, WINDOW_SIZE + 20)
                # Update the display
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        row = y // SQUARE_SIZE
                        col = x // SQUARE_SIZE

                        if row < 3 and col < 3:
                            # Check if the clicked square is empty
                            if game.board[row][col] == '':
                                # Make a move
                                game.make_move((row, col))
                                last_move = (row, col)
                                game.turn_count += 1  # Increment turn count
                                # Update the display after the player's move
                                restart_button_rect, quit_button_rect = draw_board(screen, button_font)
                                draw_moves(screen)
                                pygame.display.flip()
                                # Check for winner
                                winner = game.check_win()
                                if winner != 0:
                                    if game.player_turn == 1:
                                        display_text(screen, "O won !", font, RED, WINDOW_SIZE // 2, WINDOW_SIZE + 20)
                                    elif game.player_turn == 2:
                                        display_text(screen, "X won !", font, RED, WINDOW_SIZE // 2, WINDOW_SIZE + 20)
                                    pygame.display.flip()
                                    check = True
                                    while check:
                                        for event in pygame.event.get():
                                            if event.type == pygame.MOUSEBUTTONDOWN:
                                                if restart_button_rect.collidepoint(event.pos):
                                                    handle_restart_button_click()
                                                    check = False
                                                    break
                                                elif quit_button_rect.collidepoint(event.pos):
                                                    running = False
                                                    check = False
                                elif game.turn_count == 9:
                                    display_text(screen, "It's a tie", font, RED, WINDOW_SIZE // 2, WINDOW_SIZE + 20)
                                    pygame.display.flip()
                                    check = True
                                    while check:
                                        for event in pygame.event.get():
                                            if event.type == pygame.MOUSEBUTTONDOWN:
                                                if restart_button_rect.collidepoint(event.pos):
                                                    handle_restart_button_click()
                                                    check = False
                                                    break
                                                elif quit_button_rect.collidepoint(event.pos):
                                                    running = False
                                                    check = False
                        # Check if Restart button is clicked
                        if restart_button_rect.collidepoint(event.pos):
                            handle_restart_button_click()
                        # Check if Quit button is clicked
                        if quit_button_rect.collidepoint(event.pos):
                            handle_quit_button_click()
                            running = False
#Function to handle play vs AI                            
