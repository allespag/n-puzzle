from __future__ import annotations

from npuzzle.npuzzle import Npuzzle


class Node:
    def __init__(self, state: Npuzzle) -> None:
        self.state = state
        self.f = 0  # total cost of the node
        self.g = 0  # distance between the current node and the start node
        self.h = 0  # estimated distance from the current node to the end node

    @property
    def successors(self) -> list[Node]:
        return [Node(state) for state in self.state.successors]
