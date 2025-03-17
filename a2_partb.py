# Main Author: Dharam Mehulbhai Ghevariya, Krutin Bharatbhai Polra
# Main Reviewer: Dharam Mehulbhai Ghevariya, Krutin Bharatbhai Polra

from a1_partc import Queue
import copy
from a1_partd import overflow

# This function duplicates and returns the board. You may find this useful
def copy_board(board):
    """
    Creates and returns a deep copy of the board.

    Parameters:
    board (list of lists): The current state of the board to copy.

    Returns:
    list of lists: A deep copy of the input board.
    """
    current_board = []
    height = len(board)
    for i in range(height):
        current_board.append(board[i].copy())
    return current_board


# This function is your evaluation function for the board
def evaluate_board(board, player):
    """
    Evaluates the board state and calculates a score for the given player.

    Parameters:
    board (list of lists): The current state of the board.
    player (int): The ID of the player (1 for Player 1, -1 for Player 2).

    Returns:
    int: A score representing the board state from the perspective of the player.
         - A high positive score indicates a favorable state for the player.
         - A negative score indicates a disadvantageous state.
    """
    winningPoint = 100
    losingPoint = -100
    drawPoint = 0
    value = 0
    total = 0
    gem = 0
    for row in board:
        for cell in row:
            if cell != 0:
                if cell < 0:
                    value = -cell
                else:
                    value = cell
                total += value
                if player == 1 and cell > 0:
                    gem += value
                if player == -1 and cell < 0:
                    gem += value
    if gem == total:
        return winningPoint
    if gem == 0:
        return losingPoint
    if total == 0:
        return drawPoint
    score = (gem * 100) // total
    return score


class GameTree:
    """
    Represents a game tree for determining the best moves in the game using the minimax algorithm.

    Attributes:
    player (int): The ID of the player (1 for Player 1, -1 for Player 2).
    board (list of lists): The current state of the board.
    root (Node): The root node of the game tree.
    tree_height (int): The maximum depth of the game tree.
    """

    class Node:
        """
        Represents a node in the game tree.

        Attributes:
        board (list of lists): The state of the board at this node.
        depth (int): The depth of this node in the tree.
        player (int): The player whose turn it is at this node.
        move (tuple): The move that led to this node (row, col).
        children (list of Node): The child nodes of this node.
        score (int): The evaluation score of this node.
        tree_height (int): The maximum depth of the game tree.
        """

        def __init__(self, board, depth, player, move=None, tree_height=4):
            self.board = board
            self.depth = depth
            self.player = player
            self.move = move
            self.children = []
            self.score = None
            self.tree_height = tree_height

    def __init__(self, board, player, tree_height=4):
        """
        Initializes the game tree with a root node.

        Parameters:
        board (list of lists): The initial state of the board.
        player (int): The ID of the player (1 for Player 1, -1 for Player 2).
        tree_height (int): The maximum depth of the game tree.
        """
        self.player = player
        self.board = copy_board(board)
        self.root = self.Node(board, 0, player)
        self.tree_height = tree_height

        # Build the tree from the root node
        self.build_tree(self.root)

    def build_tree(self, node):
        """
        Recursively builds the game tree from the given node.

        Parameters:
        node (Node): The current node to expand.

        Returns:
        None
        """
        if node.depth == self.tree_height or self.is_terminal(node.board):
            node.score = evaluate_board(node.board, node.player)
            return

        opponent = -node.player
        for move in self.get_possible_moves(node.board, node.player):
            new_board = self.apply_moves(node.board, move, node.player)
            child_node = self.Node(new_board, node.depth + 1, opponent, move, self.tree_height)
            self.build_tree(child_node)
            node.children.append(child_node)

    def minimax(self, node, alpha=float('-inf'), beta=float('inf')):
        """
        Implements the minimax algorithm with alpha-beta pruning to evaluate the game tree.

        Parameters:
        node (Node): The current node to evaluate.
        alpha (float): The best value the maximizer can guarantee.
        beta (float): The best value the minimizer can guarantee.

        Returns:
        int: The evaluation score of the node.
        """
        if not node.children:
            node.score = evaluate_board(node.board, node.player)
            return node.score

        if node.depth % 2 == 0:  # Maximizer's turn
            value = float('-inf')
            for child in node.children:
                value = max(value, self.minimax(child, alpha, beta))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break  # Beta cut-off
            node.score = value
            return value
        else:  # Minimizer's turn
            value = float('inf')
            for child in node.children:
                value = min(value, self.minimax(child, alpha, beta))
                beta = min(beta, value)
                if beta <= alpha:
                    break  # Alpha cut-off
            node.score = value
            return value

    def apply_moves(self, board, move, player):
        """
        Applies a move to the board and handles overflows.

        Parameters:
        board (list of lists): The current state of the board.
        move (tuple): The move to apply (row, col).
        player (int): The player making the move.

        Returns:
        list of lists: The new state of the board after the move is applied.
        """
        new_board = copy_board(board)
        x, y = move

        # Increment the cell with the player's gem
        if new_board[x][y] == 0 or (new_board[x][y] > 0 and player == 1) or (new_board[x][y] < 0 and player == -1):
            new_board[x][y] += player

        # Create a queue for the overflow process
        overflow_queue = Queue()
        overflow_queue.enqueue(new_board)

        # Apply the overflow process
        overflow(new_board, overflow_queue)

        return new_board

    def get_possible_moves(self, board, player):
        """
        Returns all possible moves for the given player on the current board.

        Parameters:
        board (list of lists): The current state of the board.
        player (int): The player for whom the moves are being calculated.

        Returns:
        list of tuples: List of valid moves (row, col).
        """
        moves = []
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 0 or (board[i][j] > 0 and player == 1) or (board[i][j] < 0 and player == -1):
                    moves.append((i, j))
        return moves

    def is_terminal(self, board):
        """
        Checks if the board state is terminal (game over).

        Parameters:
        board (list of lists): The current state of the board.

        Returns:
        bool: True if the game is over, False otherwise.
        """
        return all(cell > 0 for row in board for cell in row) or all(cell < 0 for row in board for cell in row)

    def get_move(self):
        """
        Determines the best move for the current player using the minimax algorithm.

        Returns:
        tuple: The best move (row, col) for the current player.
        """
        best_score = float('-inf')
        best_move = None
        for child in self.root.children:
            score = self.minimax(child)
            if score > best_score:
                best_score = score
                best_move = child.move
        return best_move

    def clear_tree(self):
        """
        Clears the game tree by deleting all nodes.

        Returns:
        None
        """
        def delete_subtree(node):
            for child in node.children:
                delete_subtree(child)
            node.children = []

        delete_subtree(self.root)
        self.root = None
