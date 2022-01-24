from __future__ import annotations

from npuzzle.npuzzle import Npuzzle

COST = 1


class Node:
    def __init__(self, state: Npuzzle) -> None:
        self.state = state
        self.g = 0
        self.h = 0
        self.parent: Node | None = None

    @property
    def f(self) -> int:
        return self.g + self.h

    def __repr__(self) -> str:
        return f"Node({self.state!r}, f={self.f}, g={self.g}, h={self.h}, {self.parent}, @{hex(id(self))})"

    def __lt__(self, other: Node) -> bool:
        return self.f < other.f

    def __eq__(self, other: Node) -> bool:
        return self.__hash__() == other.__hash__()

    def __hash__(self) -> int:
        return hash(tuple(self.state.tiles))

    @property
    def successors(self) -> list[Node]:
        return [Node(state) for state in self.state.successors]

    def display_genealogy(self, ascending: bool = True) -> None:
        if ascending:
            print(self.state, end="\n\n")

        if not self.parent is None:
            self.parent.display_genealogy(ascending=ascending)

        if not ascending:
            print(self.state, end="\n\n")

    def get_genealogy_size(self) -> int | float:
        try:
            if self.parent is None:
                return 0
            else:
                return self.parent.get_genealogy_size() + 1
        except RecursionError:
            return float("-inf")
