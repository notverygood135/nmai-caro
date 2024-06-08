import copy
import math
import numpy as np
import time
import random
from game import Game


class Node:
    def __init__(self, game: Game, parent, most_recent_move: tuple):
        self.game: Game = game
        self.parent: Node = parent
        self.most_recent_move: tuple = most_recent_move
        self.children: list[Node] = []
        self.visited: int = 0
        self.evaluation: float = 0

    def get_all_possible_states(self) -> list[tuple[tuple, Game]]:
        game: Game = self.game
        states: list[tuple[tuple, Game]] = []
        # Thử từng ô còn trống
        for i in range(0, game.size):
            for j in range(0, game.size):
                if game.board[i][j] == '':
                    game.make_move((i, j))
                    states.append(((i, j), copy.deepcopy(game)))
                    game.undo_move((i, j))  # Bỏ nước đi vừa thực hiện để thử nước đi khác
        return states

    def get_random_child_node(self):
        return self.children[random.randrange(len(self.children))]

    def get_best_child(self):
        return max(self.children, key=lambda n: n.evaluation)


class Tree:
    def __init__(self, game: Game):
        self.root: Node = Node(game, None, (-1, -1))


def select_promising_node(node: Node) -> Node:
    while len(node.children) != 0:
        node = find_best_node_uct(node)
    return node


def expand_node(node: Node):
    possible_states: list[tuple, Game] = node.get_all_possible_states()
    for state in possible_states:
        new_node: Node = Node(state[1], node, state[0])
        # new_node.game.player_turn = new_node.game.get_opponent()  # might remove later
        node.children.append(new_node)


class MCTS:
    def __init__(self, game: Game):
        self.best_move: tuple = (-1, -1)
        self.game: Game = game
        self.opponent: int = game.get_opponent()
        self.node_count: int = 0

    def monte_carlo_tree_search(self, move_time):
        end: float = time.time() + move_time

        game: Game = self.game
        tree: Tree = Tree(game)
        root_node: Node = tree.root

        while time.time() < end:
            promising_node: Node = select_promising_node(root_node)
            if not promising_node.game.check_win() and promising_node.game.get_empty_squares_count() > 0:
                expand_node(promising_node)
            node_to_explore: Node = promising_node
            if len(promising_node.children) > 0:
                node_to_explore = promising_node.get_random_child_node()
            playout_result: float = self.simulate_random_playout(node_to_explore)
            self.node_count = self.node_count + 1
            backpropagation(node_to_explore, playout_result)

        best_node: Node = root_node.get_best_child()
        tree.root = best_node
        self.best_move = best_node.most_recent_move

    def simulate_random_playout(self, node: Node) -> float:
        temp_node: Node = copy.deepcopy(node)
        if temp_node.game.check_win() == self.opponent:
            return -3 - temp_node.game.get_empty_squares_count()/2
        elif temp_node.game.check_win() == self.game.player_turn:
            return 3 + temp_node.game.get_empty_squares_count()/2

        while not temp_node.game.check_win() and temp_node.game.get_empty_squares_count() > 0:
            temp_node.game.make_random_move()
        if temp_node.game.check_win() == self.opponent:
            return -3 - temp_node.game.get_empty_squares_count()
        elif temp_node.game.check_win() == self.game.player_turn:
            return 3 + temp_node.game.get_empty_squares_count()
        else:
            return 0


def uct(evaluation: float, parent_visited: int, visited: int) -> float:
    if visited == 0:
        return math.inf
    return evaluation + math.sqrt(2) * np.sqrt(np.log(parent_visited) / visited)


def find_best_node_uct(node: Node) -> Node:
    parent_visited: int = node.visited
    return max(node.children, key=lambda n: uct(n.evaluation, parent_visited, n.visited))


def backpropagation(node_to_explore: Node, playout_result: float) -> None:
    temp_node: Node = node_to_explore
    while temp_node is not None:
        temp_node.visited = temp_node.visited + 1
        temp_node.evaluation = temp_node.evaluation + playout_result
        temp_node = temp_node.parent
