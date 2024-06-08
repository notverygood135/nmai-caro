import math
from game import Game


class AlphaBeta:
    # Hàm khởi tạo được gọi mỗi khi đến lượt của bot (game.player_turn), bởi vì người sẽ luôn chọn nước đi tốt nhất nên
    # người sẽ là maximizer, bot sẽ là minimizer
    def __init__(self, game: Game):
        self.best_move: tuple = (-1, -1)
        self.game: Game = game
        self.maximizer: int = 1 if game.player_turn == 2 else 2
        self.node_count: int = 0

    # Cắt tỉa alpha beta giống minimax nhưng nó sẽ không duyệt một số nhánh mà không cho kết quả tốt hơn nhánh đã duyệt
    # mấy ô có thể xem vid này để biết thêm chi tiết https://www.youtube.com/watch?v=l-hh51ncgDI
    def alpha_beta_pruning(self, depth: int, player: int, alpha: float, beta: float):
        self.node_count = self.node_count + 1
        prune: bool = False
        game: Game = self.game

        if player == self.maximizer:
            curr_max: float = -math.inf
        else:
            curr_max: float = math.inf
        curr_best_move: tuple = (-1, -1)

        other_player: int = game.get_opponent()

        if game.check_win() == self.maximizer:
            return 1000
        elif game.check_win() != self.maximizer and game.check_win() != 0:
            return -1000
        if game.get_empty_squares_count() == 0:
            return 0
        if depth == 0:
            return game.evaluate_player(player)

        for i in range(0, game.size):
            for j in range(0, game.size):
                if game.board[i][j] == '':
                    game.make_move((i, j))
                    evaluation: float = self.alpha_beta_pruning(depth - 1, other_player, alpha, beta)
                    if player == self.maximizer:
                        if evaluation > curr_max:
                            curr_best_move = (i, j)
                            curr_max = evaluation
                        alpha = max(alpha, curr_max)
                    else:
                        if evaluation < curr_max:
                            curr_best_move = (i, j)
                            curr_max = evaluation
                        beta = min(beta, curr_max)
                    game.undo_move((i, j))
                    if beta <= alpha:
                        prune = True
                        break
            if prune:
                break
        self.best_move = curr_best_move
        return curr_max