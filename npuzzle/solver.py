from __future__ import annotations

import inspect
from queue import LifoQueue, PriorityQueue, Queue
from typing import Protocol, Type

from npuzzle.distance import Distance
from npuzzle.node import COST, Node
from npuzzle.npuzzle import Npuzzle
from npuzzle.report import Report, ReportManager


class Solver(Protocol):
    report: Report

    def run(self, start: Npuzzle, goal: Npuzzle) -> Node | None:
        ...


class AStar:
    def __init__(self, distance: Distance) -> None:
        self.open: PriorityQueue[Node] = PriorityQueue()
        self.__open_hash: set[Node] = set()
        self.close: set[Node] = set()
        self.distance: Distance = distance
        self.report: Report = Report(
            author=f"AStar with {type(self.distance).__name__}"
        )

    @ReportManager.as_result(Node.get_genealogy_size, if_failed=False)
    @ReportManager.time
    def run(self, start: Npuzzle, goal: Npuzzle) -> Node | None:
        root = Node(start)
        self.__add_to_open(root)

        while not self.open.empty():
            current = self.__remove_from_open()

            if current.state == goal:
                return current

            self.__add_to_close(current)
            successors = current.successors
            for successor in successors:
                if self.__node_in_close(successor):
                    continue
                g = current.g + COST
                if self.__node_in_open(successor):
                    if g < successor.g:
                        successor.g = g
                        successor.parent = current.parent
                else:
                    successor.g = g
                    successor.h = self.distance.compute(successor.state, goal)
                    successor.parent = current
                    self.__add_to_open(successor)
        return None

    @ReportManager.balance(2)
    def __add_to_open(self, node: Node) -> None:
        self.open.put(node)
        self.__open_hash.add(node)

    @ReportManager.balance(1)
    def __add_to_close(self, node: Node) -> None:
        self.close.add(node)

    @ReportManager.balance(-2)
    @ReportManager.count
    def __remove_from_open(self) -> Node:
        result = self.open.get()
        self.__open_hash.remove(result)
        return result

    @ReportManager.balance(-1)
    def __remove_from_close(self, node: Node) -> None:
        self.close.remove(node)

    def __node_in_close(self, node: Node) -> bool:
        return node in self.close

    def __node_in_open(self, node: Node) -> bool:
        return node in self.__open_hash


class Dijkstra:
    def __init__(self) -> None:
        self.open: PriorityQueue[Node] = PriorityQueue()
        self.__open_hash: set[Node] = set()
        self.close: set[Node] = set()
        self.report: Report = Report(author="Dijkstra")

    @ReportManager.as_result(Node.get_genealogy_size, if_failed=False)
    @ReportManager.time
    def run(self, start: Npuzzle, goal: Npuzzle) -> Node | None:
        root = Node(start)
        self.__add_to_open(root)

        while not self.open.empty():
            current = self.__remove_from_open()

            if current.state == goal:
                return current

            self.__add_to_close(current)
            successors = current.successors
            for successor in successors:
                if self.__node_in_close(successor):
                    continue
                g = current.g + COST
                if self.__node_in_open(successor):
                    if g < successor.g:
                        successor.g = g
                else:
                    successor.g = g
                    successor.parent = current
                    self.__add_to_open(successor)
        return None

    @ReportManager.balance(2)
    def __add_to_open(self, node: Node) -> None:
        self.open.put(node)
        self.__open_hash.add(node)

    @ReportManager.balance(1)
    def __add_to_close(self, node: Node) -> None:
        self.close.add(node)

    @ReportManager.balance(-2)
    @ReportManager.count
    def __remove_from_open(self) -> Node:
        result = self.open.get()
        self.__open_hash.remove(result)
        return result

    def __node_in_close(self, node: Node) -> bool:
        return node in self.close

    def __node_in_open(self, node: Node) -> bool:
        return node in self.__open_hash


class GreedySearch:
    def __init__(self, distance: Distance) -> None:
        self.open: PriorityQueue[Node] = PriorityQueue()
        self.close: set[Node] = set()
        self.distance: Distance = distance
        self.report: Report = Report(
            author=f"GreedySearch with {type(self.distance).__name__}"
        )

    @ReportManager.as_result(Node.get_genealogy_size, if_failed=False)
    @ReportManager.time
    def run(self, start: Npuzzle, goal: Npuzzle) -> Node | None:
        root = Node(start)
        self.__add_to_open(root)

        while not self.open.empty():
            current = self.__remove_from_open()

            if current.state == goal:
                return current

            self.__add_to_close(current)
            successors = current.successors
            for successor in successors:
                if self.__node_in_close(successor):
                    continue
                else:
                    successor.h = self.distance.compute(successor.state, goal)
                    successor.parent = current
                    self.__add_to_open(successor)
        return None

    @ReportManager.balance(1)
    def __add_to_open(self, node: Node) -> None:
        self.open.put(node)

    @ReportManager.balance(1)
    def __add_to_close(self, node: Node) -> None:
        self.close.add(node)

    @ReportManager.balance(-1)
    @ReportManager.count
    def __remove_from_open(self) -> Node:
        result = self.open.get()
        return result

    def __node_in_close(self, node: Node) -> bool:
        return node in self.close


class BFS:
    def __init__(self) -> None:
        self.queue: Queue[Node] = Queue()
        self.visited: set[Node] = set()
        self.report: Report = Report(author="BFS")

    @ReportManager.as_result(Node.get_genealogy_size, if_failed=False)
    @ReportManager.time
    def run(self, start: Npuzzle, goal: Npuzzle) -> Node | None:
        root = Node(start)
        self.__add_to_visited(root)
        self.__add_to_queue(root)

        while not self.queue.empty():
            current = self.__remove_from_queue()

            if current.state == goal:
                return current

            successors = current.successors

            for successor in successors:
                if not successor in self.visited:
                    successor.parent = current
                    self.__add_to_visited(successor)
                    self.__add_to_queue(successor)

    @ReportManager.balance(1)
    def __add_to_queue(self, node: Node) -> None:
        self.queue.put(node)

    @ReportManager.balance(-1)
    @ReportManager.count
    def __remove_from_queue(self) -> Node:
        return self.queue.get()

    @ReportManager.balance(1)
    def __add_to_visited(self, node: Node) -> None:
        self.visited.add(node)


class DFS:
    def __init__(self) -> None:
        self.stack: LifoQueue[Node] = LifoQueue()
        self.visited: set[Node] = set()
        self.report: Report = Report(author="DFS")

    @ReportManager.as_result(Node.get_genealogy_size, if_failed=False)
    @ReportManager.time
    def run(self, start: Npuzzle, goal: Npuzzle) -> Node | None:
        root = Node(start)
        self.__add_to_stack(root)

        while not self.stack.empty():
            current = self.__remove_from_stack()

            if current.state == goal:
                return current

            if not current in self.visited:
                self.__add_to_visited(current)

                successors = current.successors
                for successor in successors:
                    successor.parent = current
                    self.__add_to_stack(successor)

    @ReportManager.balance(1)
    def __add_to_stack(self, node: Node) -> None:
        self.stack.put(node)

    @ReportManager.balance(-1)
    @ReportManager.count
    def __remove_from_stack(self) -> Node:
        return self.stack.get()

    @ReportManager.balance(1)
    def __add_to_visited(self, node: Node) -> None:
        self.visited.add(node)


class IDAStar:
    def __init__(self, distance: Distance) -> None:
        self.path: LifoQueue[Node] = LifoQueue()
        self.distance: Distance = distance
        self.report: Report = Report(
            author=f"IDAStar with {type(self.distance).__name__}"
        )

    @ReportManager.count
    def __search(self, goal: Npuzzle, g: int, bound: int) -> Node | int | None:
        node = self.path.queue[-1]
        node.g = g
        node.h = self.distance.compute(node.state, goal)

        if node.f > bound:
            return node.f
        if node.state == goal:
            return node

        min_ = float("+inf")
        successors = node.successors
        for successor in successors:
            if not self.__node_in_path(successor):
                successor.parent = node
                self.__add_to_path(successor)

                t = self.__search(goal, node.g + COST, bound)
                if isinstance(t, Node):
                    return t
                if isinstance(t, (int, float)) and t < min_:
                    min_ = t
                self.__remove_from_path()
        if min_ == float("+inf"):
            return None
        else:
            return min_  # type: ignore

    @ReportManager.as_result(Node.get_genealogy_size, if_failed=False)
    @ReportManager.time
    def run(self, start: Npuzzle, goal: Npuzzle) -> Node | None:
        root = Node(start)
        bound = self.distance.compute(root.state, goal)
        self.__add_to_path(root)

        while True:
            t = self.__search(goal, 0, bound)
            if isinstance(t, Node) or t is None:
                return t
            else:
                bound = t

    @ReportManager.balance(1)
    def __add_to_path(self, node: Node) -> None:
        self.path.put(node)

    @ReportManager.balance(-1)
    def __remove_from_path(self) -> Node:
        return self.path.get()

    def __node_in_path(self, node: Node) -> bool:
        return any(n.state == node.state for n in self.path.queue)


# TODO
class BidirectionalSearch:
    def __init__(self, distance: Distance) -> None:
        self.distance: Distance = distance
        self.report: Report = Report(
            author=f"BidirectionalSearch with {type(self.distance).__name__}"
        )

    def run(self, start: Npuzzle, goal: Npuzzle) -> Node | None:
        raise NotImplementedError


AVAILABLE_SOLVERS: list[Type[Solver]] = [
    AStar,
    Dijkstra,
    GreedySearch,
    BFS,
    DFS,
    IDAStar,
]

DEFAULT_SOLVER: Type[Solver] = AStar


def is_informed(solver: Type[Solver]) -> bool:
    return "distance" in inspect.signature(solver).parameters
