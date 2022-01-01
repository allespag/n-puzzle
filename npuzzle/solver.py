from queue import PriorityQueue
from typing import Protocol

from npuzzle.distance import Distance
from npuzzle.node import Node
from npuzzle.npuzzle import Npuzzle


class Solver(Protocol):
    def run(self, root: Node, goal: Npuzzle) -> None:
        ...


# note: i think A* should not be here
#       so i can move import out
class AStar(Solver):
    def __init__(self, distance: Distance):
        self.open: PriorityQueue[Node] = PriorityQueue()
        self.close: list[Node] = []
        self.distance = distance

    def run(self, root: Node, goal: Npuzzle) -> None:
        self.open.put(root)

        while not self.open.empty():

            current_node = self.open.get()

            self.close.append(current_node)

            for successor in current_node.successors:
                if successor in self.close:
                    continue

                successor.g = current_node.g + 1
                successor.h = self.distance.compute(successor.state, goal)
                successor.f = successor.g + successor.h

                if successor not in self.open.queue:
                    self.open.put(successor)
