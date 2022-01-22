from __future__ import annotations

from typing import Protocol, Type

from npuzzle.npuzzle import EMPTY_TILE, Npuzzle
from npuzzle.utils import coor_to_index, index_to_coor


class Distance(Protocol):
    def compute(self, src: Npuzzle, dst: Npuzzle) -> int:
        ...


class Manhattan:
    def compute(self, src: Npuzzle, dst: Npuzzle) -> int:
        distance = 0
        for i, tile in enumerate(src.tiles):
            if tile == EMPTY_TILE:
                continue
            dst_index = dst.tiles.index(tile)
            src_x, src_y = index_to_coor(i, (src.n, src.n))
            dst_x, dst_y = index_to_coor(dst_index, (dst.n, dst.n))
            distance += abs(src_x - dst_x)
            distance += abs(src_y - dst_y)
        return distance


class TilesOutOfPlace:
    def compute(self, src: Npuzzle, dst: Npuzzle) -> int:
        return sum(a != b for a, b in zip(src.tiles, dst.tiles))


class LinearConflict:
    def compute(self, src: Npuzzle, dst: Npuzzle) -> int:
        conflict = 0

        # for i in range(src.n):
        #     src_row = src.tiles[i * src.n : (i + 1) * src.n]
        #     src_col = src.tiles[i :: src.n]
        #     dst_row = dst.tiles[i * src.n : (i + 1) * src.n]
        #     dst_col = dst.tiles[i :: src.n]

        #     for x, y in zip(src_row, dst_row):
        #         if x == 0 or x == y:
        #             continue
        #         if x in dst_row:
        #             for i

        return Manhattan().compute(src, dst) + 2 * conflict


AVAILABLE_HEURISTICS: list[Type[Distance]] = [
    Manhattan,
    TilesOutOfPlace,
]

DEFAULT_HEURISTIC: Type[Distance] = Manhattan
