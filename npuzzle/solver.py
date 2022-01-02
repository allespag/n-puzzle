from os import cpu_count
from queue import PriorityQueue
from typing import Protocol

from npuzzle.distance import Distance
from npuzzle.node import Node
from npuzzle.npuzzle import Npuzzle


class Solver(Protocol):
    def run(self, start: Npuzzle, goal: Npuzzle) -> None:
        ...


# note: i think A* should not be here
#       so i can move import out
class AStar(Solver):
    def __init__(self, distance: Distance):
        self.open: PriorityQueue[Node] = PriorityQueue()
        self.close: list[Node] = []
        self.distance = distance

    def run(self, start: Npuzzle, goal: Npuzzle) -> None:
        root = Node(start)
        self.open.put(root)

        while not self.open.empty():
            current_node = self.open.get()
            self.close.append(current_node)

            print(current_node.state.tiles, end="\n****************\n")

            if current_node.state == goal:
                print("Found!")
                return

            for successor in current_node.successors:
                for item in self.close:
                    if item.state == successor.state:
                        continue
                successor.parent = current_node
                successor.g = current_node.g + 1
                successor.h = self.distance.compute(successor.state, goal)
                successor.f = successor.g + successor.h
                for item in self.open.queue:
                    if item.state == successor.state and successor.g > item.g:
                        continue
                self.open.put(successor)

    # def run__old(self, start: Npuzzle, goal: Npuzzle) -> None:
    #     root = Node(start)
    #     self.open.put(root)

    #     while not self.open.empty():

    #         current_node = self.open.get()

    #         # print(f"{len(self.open.queue)}")
    #         # print(f"{len(self.close)}")
    #         # print(current_node.state)

    #         if current_node.state == goal:
    #             print("Found!")
    #             return

    #         for successor in current_node.successors:
    #             successor.g = current_node.g + 1
    #             successor.h = self.distance.compute(successor.state, goal)
    #             successor.f = successor.g + successor.h

    #             if any(
    #                 successor.state.tiles == node.state.tiles and successor.f < node.f
    #                 for node in self.open.queue
    #             ):
    #                 self.close.append(successor)
    #             elif any(
    #                 successor.state.tiles == node.state.tiles and successor.f < node.f
    #                 for node in self.close
    #             ):
    #                 self.close.append(successor)
    #             else:
    #                 self.open.put(successor)
    #         self.close.append(current_node)
