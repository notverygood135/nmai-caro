import math
from game import Game


class Minimax:
    # Hàm khởi tạo được gọi mỗi khi đến lượt của bot (game.player_turn), bởi vì người sẽ luôn chọn nước đi tốt nhất nên
    # người sẽ là maximizer, bot sẽ là minimizer
    def __init__(self, game: Game):
        self.best_move: tuple = (-1, -1)
        self.game: Game = game
        self.maximizer: int = 1 if game.player_turn == 2 else 2
        self.node_count: int = 0

    # Tìm nước đi tối ưu bằng minimax
    def minimax(self, depth: int, player: int) -> float:
        self.node_count = self.node_count + 1
        game: Game = self.game

        # Nếu người chơi lượt hiện tại là maximizer
        if player == self.maximizer:
            curr_max: float = -math.inf
        else:
            curr_max: float = math.inf
        curr_best_move: tuple = (-1, -1)

        # Người chơi còn lại
        other_player: int = game.get_opponent()

        # Kiểm tra xem đã kết thúc game chưa hoặc đã đến chiều sâu cuối cùng chưa
        if game.check_win() == self.maximizer:
            return 1000
        elif game.check_win() != self.maximizer and game.check_win() != 0:
            return -1000
        if game.get_empty_squares_count() == 0:
            return 0
        if depth == 0:
            return game.evaluate_player(player)

        # Thử từng ô còn trống
        for i in range(0, game.size):
            for j in range(0, game.size):
                if game.board[i][j] == '':
                    game.make_move((i, j))
                    evaluation: float = self.minimax(depth - 1, other_player)  # Mô phỏng lượt đi của người tiếp theo
                    # Nếu người chơi lượt hiện tại là maximizer thì chọn nước đi làm cho evaluation của maximizer là cao
                    # nhất
                    if player == self.maximizer:
                        if evaluation > curr_max:
                            curr_best_move = (i, j)
                            curr_max = evaluation
                    # Nếu người chơi lượt hiện tại là minimizer thì chọn nước đi làm cho evaluation của maximizer là nhỏ
                    # nhất
                    else:
                        if evaluation < curr_max:
                            curr_best_move = (i, j)
                            curr_max = evaluation
                    game.undo_move((i, j))  # Bỏ nước đi vừa thực hiện để thử nước đi khác
        self.best_move = curr_best_move
        return curr_max