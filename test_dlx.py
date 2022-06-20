import dlx
import sys

MATRIX_EMPTY = []

MATRIX_WITH_ONE_SOLUTION = [
    [0, 0, 1, 0, 1, 1, 0],
    [1, 0, 0, 1, 0, 0, 1],
    [0, 1, 1, 0, 0, 1, 0],
    [1, 0, 0, 1, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 1],
    [0, 0, 0, 1, 1, 0, 1],
]

MATRIX_WITH_THREE_SOLUTIONS = [
    [1, 0, 0, 0],
    [0, 1, 1, 0],
    [1, 0, 0, 1],
    [0, 0, 1, 1],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
]

# problem = [
#     [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
#     [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
#     [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
#     [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#     [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
#     [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
#     [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
#     [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
#     [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
# ]


# def test():
#     print(dlx.solve(problem))


if __name__ == "__main__":
    # print("engaged")
    #     # print("hello dlxlibpy")
    #     # print(dir(dlx))
    #     # print(dlx.solve(MATRIX_EMPTY))
    #     # print(dlx.solve(MATRIX_WITH_ONE_SOLUTION))
    #     # print(dlx.solve(MATRIX_WITH_THREE_SOLUTIONS))
    problem = None
    exec("problem = {}".format(sys.argv[1]))
    # print(problem)
    print(dlx.solve(problem))
#     # lt = [(0, 1), (2, 3), (3, 4)]
#     # x, y = [t[0] for t in lt], [t[1] for t in lt]
#     # print(x)
#     # print(y)
#     # print(y)
