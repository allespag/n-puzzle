from __future__ import annotations

from npuzzle.npuzzle import Npuzzle


class Node:
    def __init__(self, state: Npuzzle) -> None:
        self.state = state
        self.f = 0  # total cost of the node
        self.g = 0  # distance between the current node and the start node
        self.h = 0  # estimated distance from the current node to the end node
        self.parent: Node | None = None

    def __repr__(self) -> str:
        return f"Node({self.state!r}, f={self.f}, g={self.g}, h={self.h}, {self.parent}, @{hex(id(self))})"

    def __lt__(self, other: Node) -> bool:
        return self.f < other.f

    def __eq__(self, other: Node) -> bool:
        return self.__hash__() == other.__hash__()

    def __hash__(self) -> int:
        return id(self)

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
