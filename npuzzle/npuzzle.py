from __future__ import annotations

import copy
import random
from enum import IntEnum, auto

from npuzzle.utils import coor_in_list, coor_to_index, index_in_list, index_to_coor

EMPTY_TILE = 0
MIN_N_VALUE = 2
MAX_N_VALUE = 10


class Move(IntEnum):
    UP = 0
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()


class NNotInRangeError(Exception):
    """Exception raised when n is not between MIN_N_VALUE and MAX_N_VALUE."""

    def __init__(
        self, n: int, message: str = f"n is not in ({MIN_N_VALUE}, {MAX_N_VALUE}) range"
    ) -> None:
        self.n = n
        self.message = message
        super().__init__(self.message)


class TilesFormatError(Exception):
    """Exception raised when tiles is poorly formatted."""

    def __init__(
        self, tiles: list[int], message: str = "Tiles is poorly formatted"
    ) -> None:
        self.tiles = tiles
        self.message = message
        super().__init__(self.message)


class Npuzzle:
    def __init__(self, n: int, tiles: list[int]) -> None:
        if n < MIN_N_VALUE or n > MAX_N_VALUE:
            raise NNotInRangeError(n)
        if len(tiles) != n * n:
            raise TilesFormatError(
                tiles,
                message=f"The expected tiles size was {n * n}. ({len(tiles)} here)",
            )
        if len(tiles) != len(set(tiles)):
            raise TilesFormatError(
                tiles, message="Several occurrences of the same value found"
            )
        if any(tile not in list(range(n * n)) for tile in tiles):
            raise TilesFormatError(
                tiles,
                message=f"Tiles should only contain values between 0 and {n * n - 1}",
            )
        self.n = n
        self.tiles = tiles

    @staticmethod
    def from_file(path: str) -> Npuzzle:
        n = -1
        tiles: list[int] = []
        with open(path) as f:
            for line in f.readlines():
                line = line.split("#")[0]
                line = line.split(" ")
                line = [elem.replace("\n", "") for elem in line]
                line = list(filter(lambda x: x.isnumeric(), line))
                if not line:
                    continue
                line = [int(elem) for elem in line]
                if len(line) == 1:
                    n = line[0]
                else:
                    tiles += line
        return Npuzzle(n, tiles)

    @staticmethod
    def from_random(n: int) -> Npuzzle:
        tiles = list(range(n * n))
        random.shuffle(tiles)

        return Npuzzle(n, tiles)

    def __repr__(self) -> str:
        return f"Npuzzle({self.tiles}, n={self.n}, @{hex(id(self))})"

    def __str__(self) -> str:
        pattern = " {: <{digit}} |"
        max_digit = len(str(max(self.tiles)))
        res = "\n".join(pattern * self.n for _ in range(self.n))
        return res.format(*self.tiles, digit=max_digit)

    def __eq__(self, other: Npuzzle) -> bool:
        a = self.tiles.copy()
        b = other.tiles.copy()
        a.remove(EMPTY_TILE)
        b.remove(EMPTY_TILE)

        return a == b

    @property
    def empty_tile(self) -> int:
        return self.tiles.index(EMPTY_TILE)

    # TODO: unWRONG this
    @property
    def goal(self) -> Npuzzle:
        return Npuzzle(3, [1, 2, 3, 8, 0, 4, 7, 6, 5])
        # return Npuzzle(self.n, list(range(self.n * self.n)))

    # TODO
    @property
    def solvable(self) -> bool:
        return True

    # note: I don't know if it's the right way to do things, for now it is what it is.
    def make_move(self, move: Move) -> bool:
        moves = [
            Npuzzle.__make_up,
            Npuzzle.__make_right,
            Npuzzle.__make_down,
            Npuzzle.__make_left,
        ]
        return moves[move](self)

    def __make_up(self) -> bool:
        src = self.empty_tile
        dst = src - self.n

        if not index_in_list(dst, self.tiles):
            return False

        self.tiles[src] = self.tiles[dst]
        self.tiles[dst] = EMPTY_TILE
        return True

    def __make_right(self) -> bool:
        src_x, src_y = index_to_coor(self.empty_tile, (self.n, self.n))
        dst_x = src_x + 1
        dst_y = src_y

        if not coor_in_list((dst_x, dst_y), (self.n, self.n)):
            return False

        dst = coor_to_index((dst_x, dst_y), (self.n, self.n))

        self.tiles[self.empty_tile] = self.tiles[dst]
        self.tiles[dst] = EMPTY_TILE

        return True

    def __make_down(self) -> bool:
        src = self.empty_tile
        dst = src + self.n

        if not index_in_list(dst, self.tiles):
            return False

        self.tiles[src] = self.tiles[dst]
        self.tiles[dst] = EMPTY_TILE
        return True

    def __make_left(self) -> bool:
        src_x, src_y = index_to_coor(self.empty_tile, (self.n, self.n))
        dst_x = src_x - 1
        dst_y = src_y

        if not coor_in_list((dst_x, dst_y), (self.n, self.n)):
            return False

        dst = coor_to_index((dst_x, dst_y), (self.n, self.n))

        self.tiles[self.empty_tile] = self.tiles[dst]
        self.tiles[dst] = EMPTY_TILE

        return True

    @property
    def successors(self) -> list[Npuzzle]:
        res: list[Npuzzle] = []
        candidate = copy.deepcopy(self)
        for move in Move:
            success = candidate.make_move(move)
            if success:
                res.append(candidate)
                candidate = copy.deepcopy(self)
        return res
