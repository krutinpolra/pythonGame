#   Author: Catherine Leung
#   This is the game that you will code the bots to play.  You can also play against your bot
#   To run the game you will need pygames installed.  See: https://pypi.org/project/pygame/
#   Once you have pygames, you can run the game by using the command:
#   python game.py
#   
#   the gem images used are from opengameart.org by qubodup
#   https://opengameart.org/content/rotating-crystal-animation-8-step,
#   https://creativecommons.org/licenses/by/3.0/

# Main Author for new feature: Dharam Mehulbhai Ghevariya, Krutin Bharatbhai Polra
# Main Reviewer for new feature: Dharam Mehulbhai Ghevariya, Krutin Bharatbhai Polra

import pygame
import sys
import math
import copy  # Import copy to use deepcopy

from a1_partc import Stack  # Import Stack for Undo functionality
from a1_partd import overflow
from a1_partc import Queue
from player1 import PlayerOne
from player2 import PlayerTwo

class Dropdown:
    def __init__(self, x, y, width, height, options):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.options = options
        self.current_option = 0

    def draw(self, window):
        pygame.draw.rect(window, BLACK, (self.x, self.y, self.width, self.height), 2)
        font = pygame.font.Font(None, 36)
        text = font.render(self.options[self.current_option], 1, BLACK)
        window.blit(text, (self.x + 5, self.y + 5))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if self.x < x < self.x + self.width and self.y < y < self.y + self.height:
                self.current_option = (self.current_option + 1) % len(self.options)

    def get_choice(self):
        return self.current_option

class Board:
    def __init__(self,width,height, p1_sprites, p2_sprites):
        self.width = width
        self.height = height
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.p1_sprites = p1_sprites
        self.p2_sprites = p2_sprites
        self.board[0][0] = 1
        self.board[self.height-1][self.width-1] = -1
        self.turn = 0

    def get_board(self):
        current_board = []
        for i in range(self.height):
            current_board.append(self.board[i].copy())
        return current_board

    def valid_move(self, row, col, player):
        """
        Checks if a move is valid for the given player.

        Parameters:
        row (int): Row index of the move.
        col (int): Column index of the move.
        player (int): Player ID (1 for Player 1, -1 for Player 2).

        Returns:
        bool: True if the move is valid, False otherwise.
        """
        if (
            0 <= row < self.height
            and 0 <= col < self.width
            and (self.board[row][col] == 0 or self.board[row][col] / abs(self.board[row][col]) == player)
        ):
            return True
        return False

    def get_valid_moves(self, player):
        """
        Gets all valid moves for the given player.

        Parameters:
        player (int): Player ID (1 for Player 1, -1 for Player 2).

        Returns:
        list of tuples: List of (row, col) positions that are valid moves.
        """
        valid_moves = []
        for row in range(self.height):
            for col in range(self.width):
                if self.valid_move(row, col, player):
                    valid_moves.append((row, col))
        return valid_moves

    def add_piece(self, row, col, player):
        if self.valid_move(row, col, player):
            self.board[row][col] += player
            self.turn += 1
            return True
        return False

    def check_win(self):
        if(self.turn > 0):
            num_p1 = 0
            num_p2 = 0
            for i in range(self.height):
                for j in range(self.width):
                    if(self.board[i][j] > 0):
                        if num_p2 > 0:
                            return 0
                        num_p1 += 1
                    elif(self.board[i][j] < 0):
                        if num_p1 > 0:
                            return 0
                        num_p2 += 1
            if(num_p1 == 0):
                return -1
            if(num_p2== 0):
                return 1
        return 0

    def do_overflow(self,q):
        oldboard = []
        for i in range(self.height):
            oldboard.append(self.board[i].copy())
        numsteps = overflow(self.board, q)
        if(numsteps != 0):
            self.set(oldboard)
        return numsteps
    
    def set(self, newboard):
        for row in range(self.height):
            for col in range(self.width):
                self.board[row][col] = newboard[row][col]

    def draw(self, window, frame):
        for row in range(GRID_SIZE[0]):
            for col in range(GRID_SIZE[1]):
                rect = pygame.Rect(col * CELL_SIZE + X_OFFSET, row * CELL_SIZE+Y_OFFSET, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(window, BLACK, rect, 1)
        for row in range(self.height):
            for col in range(self.width):
                if self.board[row][col] != 0:
                    rpos = row * CELL_SIZE + Y_OFFSET
                    cpos = col * CELL_SIZE + X_OFFSET
                    if self.board[row][col] > 0:
                        sprite = p1_sprites
                    else:
                        sprite = p2_sprites
                    if abs(self.board[row][col]) == 1:
                        cpos += CELL_SIZE //2 - 16
                        rpos += CELL_SIZE //2 - 16
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                    elif abs(self.board[row][col]) == 2:
                        cpos += CELL_SIZE //2 - 32
                        rpos += CELL_SIZE //2 - 16
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        cpos += 32
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))

                    elif abs(self.board[row][col]) == 3:
                        cpos += CELL_SIZE //2 - 16
                        rpos += 8
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        cpos = col * CELL_SIZE + X_OFFSET + CELL_SIZE //2 - 32
                        rpos += CELL_SIZE //2
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        cpos += 32
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                    elif abs(self.board[row][col]) == 4:
                        cpos += CELL_SIZE //2 - 32
                        rpos += 8
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        rpos += CELL_SIZE //2
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        cpos += 32
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        rpos -= CELL_SIZE //2
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))


# Constants
GRID_SIZE = (5, 6)
CELL_SIZE = 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
X_OFFSET = 0
Y_OFFSET = 100
HIGHLIGHT_COLOR = (0, 255, 0)  # Green for valid moves
FULL_DELAY = 5

p1spritesheet = pygame.image.load('blue.png')
p2spritesheet = pygame.image.load('pink.png')
p1_sprites = []
p2_sprites = []

player_id = [1 , -1]

for i in range(8):
    curr_sprite = pygame.Rect(32*i,0,32,32)
    p1_sprites.append(p1spritesheet.subsurface(curr_sprite))
    p2_sprites.append(p2spritesheet.subsurface(curr_sprite))    

frame = 0

# Initialize Pygame
pygame.init()
window = pygame.display.set_mode((1200,800))

pygame.font.init()
font = pygame.font.Font(None, 36)  # Change the size as needed
bigfont = pygame.font.Font(None, 108)

# Create the game board
player1_dropdown = Dropdown(900, 50, 200, 50, ['Human', 'AI'])
player2_dropdown = Dropdown(900, 110, 200, 50, ['Human', 'AI'])

undo_stack = Stack()  # Stack for Undo functionality
undo_button = pygame.Rect(900, 300, 200, 50)  # Undo button position

status=["",""]
current_player = 0
board = Board(GRID_SIZE[1], GRID_SIZE[0], p1_sprites, p2_sprites)

running = True
overflow_boards = Queue()
overflowing = False
numsteps = 0
has_winner = False
bots = [PlayerOne(), PlayerTwo()]
grid_col = -1
grid_row = -1
choice = [None, None]
selected_cell = None  # For highlight feature

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            player1_dropdown.handle_event(event)
            player2_dropdown.handle_event(event)
            choice[0] = player1_dropdown.get_choice()
            choice[1] = player2_dropdown.get_choice()

            # Handle Undo Button Click
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row = (y - Y_OFFSET) // CELL_SIZE
                col = (x - X_OFFSET) // CELL_SIZE
                if 0 <= row < GRID_SIZE[0] and 0 <= col < GRID_SIZE[1]:
                    selected_cell = (row, col)  # Set the selected cell
                    
                if undo_button.collidepoint(x, y):  # Undo button clicked
                    if len(undo_stack) >= 2:  # Ensure at least two moves are available to undo
                        undo_stack.pop()  # Undo AI's move
                        previous_board = undo_stack.pop()  # Undo human's move
                        board.set(previous_board)  # Restore board state
                        current_player = (current_player + 1) % 2  # Revert to human's turn
                        status[1] = "Undo successful!"
                    elif len(undo_stack) == 1:  # Special case: Only one move to undo
                        previous_board = undo_stack.pop()
                        board.set(previous_board)
                        current_player = 0  # Revert to human's turn
                        status[1] = "Undo successful (1 move)!"
                    else:
                        status[1] = "No moves to undo!"

                else:
                    row = y - Y_OFFSET
                    col = x - X_OFFSET
                    grid_row, grid_col = row // CELL_SIZE, col // CELL_SIZE

    win = board.check_win()
    if win != 0:
        winner = 1 if win == 1 else 2
        has_winner = True

    if not has_winner:
        if overflowing:
            status[0] = "Overflowing"
            if not overflow_boards.is_empty():
                if repeat_step == FULL_DELAY:
                    next = overflow_boards.dequeue()
                    board.set(next)
                    repeat_step = 0
                else:
                    repeat_step += 1
            else:
                overflowing = False
                current_player = (current_player + 1) % 2
        else:
            status[0] = f"Player {current_player + 1}'s turn"
            make_move = False
            if choice[current_player] == 1:  # AI's turn
                grid_row, grid_col = bots[current_player].get_play(board.get_board())
                status[1] = f"Bot chose row {grid_row}, col {grid_col}"
                if board.valid_move(grid_row, grid_col, player_id[current_player]):
                    make_move = True
            else:  # Human's turn
                if board.valid_move(grid_row, grid_col, player_id[current_player]):
                    make_move = True

            if make_move:
                undo_stack.push(copy.deepcopy(board.get_board()))  # Save state before move
                board.add_piece(grid_row, grid_col, player_id[current_player])
                numsteps = board.do_overflow(overflow_boards)
                if numsteps != 0:
                    overflowing = True
                    repeat_step = 0
                else:
                    current_player = (current_player + 1) % 2
                grid_row = -1
                grid_col = -1

    # Draw the game board
    window.fill(WHITE)
    board.draw(window, frame)
    window.blit(p1_sprites[math.floor(frame)], (850, 60))
    window.blit(p2_sprites[math.floor(frame)], (850, 120))
    frame = (frame + 0.5) % 8

    # Highlight valid moves
    if selected_cell:
        valid_moves = board.get_valid_moves(player_id[current_player])
        for move in valid_moves:
            row, col = move
            rect = pygame.Rect(
                col * CELL_SIZE + X_OFFSET, row * CELL_SIZE + Y_OFFSET, CELL_SIZE, CELL_SIZE
            )
            pygame.draw.rect(window, HIGHLIGHT_COLOR, rect, 3)

    # Draw Undo Button
    pygame.draw.rect(window, BLACK, undo_button, 2)
    undo_text = font.render("Undo Move", True, BLACK)
    window.blit(undo_text, (undo_button.x + 10, undo_button.y + 10))

    player1_dropdown.draw(window)
    player2_dropdown.draw(window)

    if not has_winner:
        text = font.render(status[0], True, (0, 0, 0))
        window.blit(text, (X_OFFSET, 750))
        text = font.render(status[1], True, (0, 0, 0))
        window.blit(text, (X_OFFSET, 700))
    else:
        text = bigfont.render(f"Player {winner} wins!", True, (0, 0, 0))
        window.blit(text, (300, 250))

    pygame.display.update()
    pygame.time.delay(100)

pygame.quit()
sys.exit()
