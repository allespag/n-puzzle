from __future__ import annotations

from enum import IntEnum, auto
from random import shuffle
from typing import Any


EMPTY_TILE = 0
MIN_N_VALUE = 2
MAX_N_VALUE = 10

def index_in_list(index: int, l: list[Any]) -> bool:
    return 0 <= index < len(l)


def coor_in_list(coor: tuple[int, int], shape: tuple[int, int], l: list[Any]) -> bool:
    max_x, max_y = shape
    x, y = coor

    return 0 <= x < max_x and 0 <= y < max_y


class Move(IntEnum):
    UP = 0
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()


class NNotInRangeError(Exception):
    """Exception raised when n is not between MIN_N_VALUE and MAX_N_VALUE."""

    def __init__(self, n: int, message: str = f"n is not in ({MIN_N_VALUE}, {MAX_N_VALUE}) range") -> None:
        self.n = n
        self.message = message
        super().__init__(self.message)


class TilesFormatError(Exception):
    """Exception raised when tiles is poorly formatted."""

    def __init__(self, tiles: list[int], message: str = "Tiles is poorly formatted") -> None:
        self.tiles = tiles
        self.message = message
        super().__init__(self.message)


class Npuzzle:
    def __init__(self, n: int, tiles: list[int]) -> None:
        if n < MIN_N_VALUE or n > MAX_N_VALUE:
            raise NNotInRangeError(n)
        if len(tiles) != n * n:
            raise TilesFormatError(tiles, message=f"The expected tiles size was {n * n}. ({len(tiles)} here)")
        if len(tiles) != len(set(tiles)):
            raise TilesFormatError(tiles, message="Several occurrences of the same value found")
        if any(tile not in list(range(n * n)) for tile in tiles):
            raise TilesFormatError(tiles, message=f"Tiles should only contain values between 0 and {n * n - 1}")
        self.n = n
        self.tiles = tiles

    @staticmethod
    def from_file(path: str) -> Npuzzle:
        pass


    @staticmethod
    def from_random(n: int) -> Npuzzle:
        tiles = list(range(n * n))
        shuffle(tiles)

        return Npuzzle(n, tiles)


    def __str__(self) -> str:
        pattern = " {: <{digit}} |"
        max_digit = len(str(max(self.tiles)))
        res = "\n".join(pattern * self.n for _ in range(self.n))
        return res.format(*self.tiles, digit=max_digit)

    # note: I don't know if it's the right way to do things, for now it is what it is.
    def make_move(self, move: Move) -> bool:
        methods = [
            Npuzzle.__make_up,
            Npuzzle.__make_right,
            Npuzzle.__make_down,
            Npuzzle.__make_left,
        ]
        return methods[move](self)


    def __make_up(self) -> bool:
        src = self.empty_tile
        dst = src - self.n

        if not index_in_list(dst, self.tiles):
            return False
        
        self.tiles[src] = self.tiles[dst]
        self.tiles[dst] = EMPTY_TILE
        return True


    def __make_right(self) -> bool:
        src_x = self.empty_tile % self.n
        dst_x = src_x + 1
        dst_y = self.empty_tile // self.n        

        if not coor_in_list((dst_x, dst_y), (self.n, self.n), self.tiles):
            return False

        dst = dst_y * self.n + dst_x

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
        src_x = self.empty_tile % self.n
        dst_x = src_x - 1
        dst_y = self.empty_tile // self.n        

        if not coor_in_list((dst_x, dst_y), (self.n, self.n), self.tiles):
            return False

        dst = dst_y * self.n + dst_x

        self.tiles[self.empty_tile] = self.tiles[dst]
        self.tiles[dst] = EMPTY_TILE  

        return True

    @property
    def empty_tile(self) -> int:
        return self.tiles.index(EMPTY_TILE)
