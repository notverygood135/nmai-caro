from game import Game
def test(case: int) -> None:
    results: dict = {0: 0, 1: 0, 2: 0}
    for i in range(case):
        game = Game(3)
        result: int = game.start_game()
        results[result] = results[result] + 1
        del game
    print(results)


# Tham số của hàm test là số test case nó sẽ chạy
if __name__ == '__main__':
    test(1)
1