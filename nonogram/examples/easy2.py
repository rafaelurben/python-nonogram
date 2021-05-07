X = False
O = True
N = None

gamedata = {
    "xinfo": [
        [1, 1, 2, 1, 1],
        [1, 1, 2, 1],
        [1, 1, 2, 1],
        [4, 1],
        [3],
        [1],
        [1, 1],
        [1],
        [1],
        [10],
    ],
    "yinfo": [
        [1, 1],
        [1, 1],
        [1, 1, 1, 1],
        [1, 1, 1],
        [1, 2, 1],
        [2, 2, 1],
        [9],
        [1, 1, 1, 1],
        [1, 1, 1],
        [1, 1, 1],
    ],
    "board": [
        [N, N, N, N, N, N, N, N, X, N],
        [N, N, X, N, X, N, N, N, N, X],
        [N, X, N, X, N, X, N, N, N, N],
        [N, N, N, N, N, N, N, X, N, N],
        [N, X, X, N, N, N, N, N, N, N],
        [X, X, X, N, N, N, N, N, X, X],
        [N, X, N, X, X, X, N, X, X, X],
        [X, N, N, N, N, N, N, X, X, X],
        [X, N, X, N, N, X, N, N, X, X],
        [N, N, N, N, N, N, N, N, N, N],
    ]
}
