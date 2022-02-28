from __future__ import annotations

from typing import Protocol, Type

from npuzzle.npuzzle import EMPTY_TILE, Npuzzle
from npuzzle.utils import index_to_coor


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


class TilesOutOfRowCol:
    def compute(self, src: Npuzzle, dst: Npuzzle) -> int:
        src_rows: list[list[int]] = []
        dst_rows: list[list[int]] = []
        src_cols: list[list[int]] = []
        dst_cols: list[list[int]] = []
        for i in range(src.n):
            src_rows.append(src.tiles[i * src.n : (i + 1) * src.n])
            src_cols.append(src.tiles[i :: src.n])
            dst_rows.append(dst.tiles[i * src.n : (i + 1) * src.n])
            dst_cols.append(dst.tiles[i :: src.n])

        distance = 0
        for src_row, dst_row in zip(src_rows, dst_rows):
            distance += sum(tile not in dst_row for tile in src_row)
        for src_col, dst_col in zip(src_cols, dst_cols):
            distance += sum(tile not in dst_col for tile in src_col)

        return distance


# TODO
class LinearConflict:
    def __count_conflict(self, src_row: list[int], dst_row: list[int]) -> int:
        conflict = 0

        for j in range(len(src_row)):
            if src_row[j] == EMPTY_TILE or src_row[j] not in dst_row:
                continue
            for k in range(j + 1, len(src_row)):
                if src_row[k] == EMPTY_TILE or src_row[k] not in dst_row:
                    continue
                goal_k_index = dst_row.index(src_row[k])
                if j == goal_k_index:
                    conflict += 1

        return conflict

    def compute(self, src: Npuzzle, dst: Npuzzle) -> int:
        src_rows: list[list[int]] = []
        dst_rows: list[list[int]] = []
        src_cols: list[list[int]] = []
        dst_cols: list[list[int]] = []
        for i in range(src.n):
            src_rows.append(src.tiles[i * src.n : (i + 1) * src.n])
            src_cols.append(src.tiles[i :: src.n])
            dst_rows.append(dst.tiles[i * src.n : (i + 1) * src.n])
            dst_cols.append(dst.tiles[i :: src.n])

        conflict = 0
        for i in range(src.n):
            conflict += self.__count_conflict(src_rows[i], dst_rows[i])
            conflict += self.__count_conflict(src_cols[i], dst_cols[i])

        return Manhattan().compute(src, dst) + 2 * conflict


AVAILABLE_HEURISTICS: list[Type[Distance]] = [
    Manhattan,
    TilesOutOfPlace,
    TilesOutOfRowCol,
]

DEFAULT_HEURISTIC: Type[Distance] = Manhattan
