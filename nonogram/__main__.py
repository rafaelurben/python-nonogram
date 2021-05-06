"A nonogram bot in Python"

from nonogram.game import NonogramGame

X = False
O = True
N = None


game = NonogramGame(
    xinfo=[
        [5],
        [1, 4],
        [2, 1, 1],
        [2, 1, 1],
        [3, 1],
        [3, 3, 1],
        [1, 5, 2],
        [10],
        [1, 1, 4],
        [3, 4],
    ],
    yinfo=[
        [5],
        [1, 1, 1],
        [4, 1],
        [1, 3],
        [7],
        [1, 2, 3],
        [2, 5],
        [4, 3],
        [2, 4],
        [10],
    ],
    board=[
        [N, N, N, N, X, N, N, N, N, N],
        [N, N, X, X, N, N, N, N, N, N],
        [N, X, N, N, N, N, X, N, X, N],
        [N, N, X, X, N, N, N, N, X, N],
        [X, X, N, N, N, N, N, X, X, N],
        [N, N, N, N, N, N, N, N, X, N],
        [N, X, N, N, N, N, N, N, N, N],
        [N, N, N, N, N, N, N, N, N, N],
        [N, N, X, N, X, X, N, N, N, N],
        [N, N, N, X, N, X, N, N, N, N],
    ]
)
game.print()
game.solve()
game.print()
