from __future__ import annotations

from typing import Protocol

from npuzzle.npuzzle import Npuzzle
from npuzzle.utils import index_to_coor


class Distance(Protocol):
    def compute(self, src: Npuzzle, dst: Npuzzle) -> int:
        ...


class Manhattan:
    def compute(self, src: Npuzzle, dst: Npuzzle) -> int:
        distance = 0
        for i, tile in enumerate(src.tiles):
            dst_index = dst.tiles.index(tile)
            src_x, src_y = index_to_coor(i, (src.n, src.n))
            dst_x, dst_y = index_to_coor(dst_index, (dst.n, dst.n))
            distance += abs(src_x - dst_x)
            distance += abs(src_y - dst_y)
        return distance


class TilesOutOfPlace:
    def compute(self, src: Npuzzle, dst: Npuzzle) -> int:
        return sum(a != b for a, b in zip(src.tiles, dst.tiles))


AVAILABLE_HEURISTICS: list[Distance] = [
    Manhattan,
    TilesOutOfPlace,
]

DEFAULT_HEURISTIC: Distance = Manhattan
