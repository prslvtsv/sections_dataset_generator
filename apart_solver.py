# -*- coding: utf-8 -*-
"""Script to solve every possible exact cover solution

Runs from Grasshopper in terminal unsing python 3.9
(dependensies - just numpy, as far as I know)

GH prepares board and tiles indexes and pushes them as execution
arguments

Created on 21 Jun 2022

@author: prslvtsv
"""
import dlx
import sys
import argparse
from polyomino.board import Rectangle
from polyomino.tileset import Tileset
from polyomino.problem import TilingProblem
from gblock.elements.matrix import SpacialMatrix

TEST_FLOOR = [
    (0, 0),
    (0, 1),
    (0, 2),
    (1, 0),
    (1, 1),
    (1, 2),
    (1, 3),
    (2, 0),
    (2, 1),
    (2, 2),
    (2, 3),
]

TEST_APT = [
    [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)],
    [(0, 0), (0, 1), (0, 2), (1, 1), (1, 2)],
    [(0, 0), (0, 1), (0, 2), (1, 2)],
    [(0, 0), (0, 1), (0, 2)],
    [(0, 0), (0, 1)],
]


def board_from_indexes(indexes):
    bnd = SpacialMatrix.bound_indexes(indexes)
    shp = SpacialMatrix.shape_from_bound(bnd)
    si, sj = shp

    removed = []
    checkIdx = []

    for i in range(si):
        bnd = SpacialMatrix.bound_indexes(indexes)
        shp = SpacialMatrix.shape_from_bound(bnd)
        checkIdx = []
        si, sj = shp
        for i in range(si):
            for j in range(sj):
                checkIdx.append((i, j))
    cellsToRemove = list(set(checkIdx) ^ set(indexes))
    return Rectangle(shp[0], shp[1]).remove_all(cellsToRemove)


def compute_combinations(board, aparts):
    tileset = Tileset([], [], aparts, True)
    combinations = TilingProblem(board, tileset)
    combinations.make_problem()
    return combinations.key


def compute_cover_problem(board, combinations):
    return [[1 if cell in comb else 0 for cell in board] for comb in combinations]


def run_dlx_sim(board_idx, apt_sets, index=False):
    board = board_from_indexes(board_idx)
    comb = compute_combinations(board, apt_sets)
    problem = compute_cover_problem(board.squares, comb)
    solution = [sorted(s) for s in dlx.solve(problem)]

    if index:
        cells = [[comb[t] for t in tiling] for tiling in solution]
        indexes = solution
        return cells, indexes
    return [[comb[t] for t in tiling] for tiling in solution]


def solve_possible_tiling(board=TEST_FLOOR, apt_set=TEST_APT):
    cells, idxGroups = run_dlx_sim(board, apt_set, True)
    return cells, idxGroups


def run_test():

    aptLayouts = run_dlx_sim(TEST_FLOOR, TEST_APT)
    # for s in aptLayouts:
    #     for t in s:
    #
    #         mtx = SpacialMatrix().from_indexes(t)
    #         print(mtx)
    #     print()
    return aptLayouts


def prepare_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--board", "-bd", type=str, required=True)
    parser.add_argument("--aparts", "-ap", type=str, required=True)
    return parser.parse_args()


if __name__ == "__main__":

    if len(sys.argv) < 2:
        run_test()
    else:
        args = prepare_args()
        # print(args.board)
        board, aparts = None, None
        exec("board = {}".format(args.board.strip()))
        exec("aparts = {}".format(args.aparts.strip()))
        #
        solution = run_dlx_sim(board, aparts)
        print(solution)
    # print(problem)
    # problem = None
    # exec("problem = {}".format(sys.argv[1]))
    # print(dlx.solve(problem))
