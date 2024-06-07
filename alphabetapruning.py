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