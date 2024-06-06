import copy
import math
import time

import numpy as np
import random


class Game:
    def __init__(self, size: int) -> None:
        self.size: int = size
        self.board: np.ndarray = np.array([['' for _ in range(0, size)] for _ in range(0, size)])
        self.turn_count: int = 0  # Số lượt đã chơi
        self.player_turn: int = 1  # Lượt hiện tại, 1 nếu là x, 2 nếu là o

    def print_board(self) -> None:
        board_string: str = ''
        for row in self.board:
            board_string = board_string + '|'
            for square in row:
                if square == '':
                    board_string = board_string + '_|'
                else:
                    board_string = board_string + square + '|'
            board_string = board_string + '\n'
        print(board_string)

    # Kiểm tra điều kiện thắng theo hàng và cột
    def check_rows(self) -> int:
        for row in self.board:
            if (row == 'x').sum() == 3:
                return 1
            elif (row == 'o').sum() == 3:
                return 2
        # Chuyển vị ma trận để kiểm tra theo cột
        for row in np.transpose(self.board):
            if (row == 'x').sum() == 3:
                return 1
            elif (row == 'o').sum() == 3:
                return 2
        return 0

    # Kiểm tra điều kiện thắng theo đường chéo
    def check_diagonals(self) -> int:
        winner: str = ''
        board: np.ndarray = self.board
        if len(set([board[i][i] for i in range(len(board))])) == 1 and board[0][0] != '':
            winner = board[0][0]
        if len(set([board[i][len(board) - i - 1] for i in range(len(board))])) == 1 \
                and board[0][len(board) - 1] != '':
            winner = board[0][len(board) - 1]
        if winner == 'x':
            return 1
        elif winner == 'o':
            return 2
        else:
            return 0

    # Kiểm tra điều kiện thắng, 1 nếu x, 2 nếu o, 0 nếu hoà/chưa có người thắng
    def check_win(self) -> int:
        result = self.check_rows()
        if result != 0:
            return result
        return self.check_diagonals()

    # Thay 1 ô trên bàn cờ bằng x hoặc o
    def make_move(self, position: tuple) -> None:
        if self.player_turn == 1:
            self.board[position[0]][position[1]] = 'x'
        else:
            self.board[position[0]][position[1]] = 'o'
        self.player_turn = self.get_opponent()

    # Bỏ 1 nước đi trên bàn cờ
    def undo_move(self, position: tuple) -> None:
        self.board[position[0]][position[1]] = ''
        self.player_turn = self.get_opponent()

    # Người dùng thực hiện nước đi tiếp theo
    def make_human_move(self) -> None:
        finished: bool = False
        while not finished:
            player_move = input("Make your move: ")
            [x, y] = player_move.split(' ')
            x = int(x)
            y = int(y)
            if x < 0 or x > len(self.board) - 1 or y < 0 or y > len(self.board) - 1 or self.board[x][y] != '':
                print('Invalid move!')
                continue
            finished = True
            self.make_move((x, y))

    # Máy thực hiện nước đi ngẫu nhiên
    def make_random_move(self) -> None:
        finished: bool = False
        while not finished:
            x = random.randint(0, len(self.board) - 1)
            y = random.randint(0, len(self.board) - 1)
            if self.board[x][y] != '':
                continue
            finished = True
            self.make_move((x, y))

    # Máy thực hiện nước đi có não
    def make_smart_move(self) -> None:
        # self.print_board()

        best_move: tuple = self.find_best_move_minimax()
        # best_move: tuple = self.find_best_move_alphabeta()
        # best_move: tuple = self.find_best_move_mcts()

        if best_move == (-1, -1):  # Nếu vì lí do nào đó không tìm được nước đi tối ưu
            self.make_random_move()
        else:
            self.make_move(best_move)

    def make_smart_move1(self) -> None:
        # self.print_board()

        # best_move: tuple = self.find_best_move_minimax()
        best_move: tuple = self.find_best_move_alphabeta()
        # best_move: tuple = self.find_best_move_mcts()

        if best_move == (-1, -1):  # Nếu vì lí do nào đó không tìm được nước đi tối ưu
            self.make_random_move()
        else:
            self.make_move(best_move)

    def make_smart_move2(self) -> None:
        # self.print_board()

        # best_move: tuple = self.find_best_move_minimax()
        # best_move: tuple = self.find_best_move_alphabeta()
        best_move: tuple = self.find_best_move_mcts()

        if best_move == (-1, -1):  # Nếu vì lí do nào đó không tìm được nước đi tối ưu
            self.make_random_move()
        else:
            self.make_move(best_move)

    # Bắt đầu lượt
    def start_turn(self) -> None:
        if self.player_turn == 1:
            self.make_human_move()
            # self.make_random_move()
            # self.make_smart_move()
        else:
            # self.make_human_move()
            # self.make_random_move()
            self.make_smart_move()

    # Bắt đầu game
    def start_game(self) -> int:
        while not self.check_win() and self.turn_count != self.size * self.size:
            self.print_board()
            self.start_turn()
            self.turn_count = self.turn_count + 1
        self.print_board()
        if self.check_win() == 1:
            print('x wins')
        elif self.check_win() == 2:
            print('o wins')
        else:
            print('it\'s a tie')
        return self.check_win()

    def get_empty_squares_count(self) -> int:
        count: int = 0
        for row in self.board:
            for square in row:
                if square == '':
                    count = count + 1
        return count

    def get_opponent(self) -> int:
        return 3 - self.player_turn
    
     # Hàm đánh giá
    def evaluate_player(self, player: int) -> int:
        horizontal_evaluation: tuple = self.evaluate_horizontal(player)
        diagonal_evaluation: tuple = self.evaluate_diagonal(player)
        return horizontal_evaluation[0] + diagonal_evaluation[0] - horizontal_evaluation[1] - diagonal_evaluation[1]

    # Đánh giá theo hàng ngang và hàng dọc
    def evaluate_horizontal(self, player: int) -> tuple:
        score_x: int = 0
        score_o: int = 0
        for row in self.board:
            if (row == 'x').sum() == 2 and player == 1:
                score_x = score_x + 3 + self.get_empty_squares_count()
            elif (row == 'o').sum() == 2 and player == 2:
                score_o = score_o + 3 + self.get_empty_squares_count()
            elif (row == 'x').sum() == 1 and (row == 'o').sum() == 0:
                score_x = score_x + 1
            elif (row == 'o').sum() == 1 and (row == 'x').sum() == 0:
                score_o = score_o + 1
        for row in np.transpose(self.board):
            if (row == 'x').sum() == 2 and player == 1:
                score_x = score_x + 3 + self.get_empty_squares_count()
            elif (row == 'o').sum() == 2 and player == 2:
                score_o = score_o + 3 + self.get_empty_squares_count()
            elif (row == 'x').sum() == 1 and (row == 'o').sum() == 0:
                score_x = score_x + 1
            elif (row == 'o').sum() == 1 and (row == 'x').sum() == 0:
                score_o = score_o + 1
        return score_x, score_o

    # Đánh giá theo đường chéo
    def evaluate_diagonal(self, player: int) -> tuple:
        score_x: int = 0
        score_o: int = 0
        left_to_right_diagonal: np.ndarray = \
            np.array([self.board[i][i] for i in range(self.size)])
        right_to_left_diagonal: np.ndarray = \
            np.array([self.board[i][self.size - i - 1] for i in range(self.size)])
        if (left_to_right_diagonal == 'x').sum() == 2 or (right_to_left_diagonal == 'x').sum() == 2 and player == 1:
            score_x = score_x + 3 + self.get_empty_squares_count()
        elif (left_to_right_diagonal == 'o').sum() == 2 or (right_to_left_diagonal == 'o').sum() == 2 and player == 2:
            score_o = score_o + 3 + self.get_empty_squares_count()
        elif (left_to_right_diagonal == 'x').sum() == 1 and (left_to_right_diagonal == 'o').sum() == 0\
                or (right_to_left_diagonal == 'x').sum() == 1 and (right_to_left_diagonal == 'o').sum() == 0:
            score_x = score_x + 1
        elif (left_to_right_diagonal == 'o').sum() == 1 and (left_to_right_diagonal == 'x').sum() == 0\
                or (right_to_left_diagonal == 'o').sum() == 1 and (right_to_left_diagonal == 'x').sum() == 0:
            score_o = score_o + 1
        return score_x, score_o