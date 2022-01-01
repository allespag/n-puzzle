from npuzzle.distance import Manhattan
from npuzzle.node import Node
from npuzzle.npuzzle import Move, Npuzzle
from npuzzle.solver import AStar


def test_make_move(n: int) -> None:
    """Test Npuzzle.make_move"""

    puzzle = Npuzzle.from_random(n)
    res = True

    while True:
        if res:
            print(puzzle, end="\n-------------------------\n")
        else:
            print("ERROR")
        move = int(input(">"))
        res = puzzle.make_move(Move(move))


def main() -> None:
    """Main function."""

    puzzle = Npuzzle.from_random(5)
    goal = puzzle.goal

    solver = AStar(Manhattan())
    solver.run(Node(puzzle), goal)


if __name__ == "__main__":
    main()
