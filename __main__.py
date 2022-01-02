from npuzzle.distance import Manhattan
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


def test_manhattan_distance() -> None:
    """Test Manhattan.compute"""

    puzzle = Npuzzle(3, [1, 2, 5, 3, 0, 6, 7, 4, 8])
    goal = Npuzzle(3, [1, 2, 3, 4, 5, 6, 7, 8, 0])
    distance = Manhattan().compute(puzzle, goal)

    print(f"Manhattan distance = {distance}")


def main() -> None:
    """Main function."""

    puzzle = Npuzzle.from_random(3)
    goal = puzzle.goal

    print(puzzle)

    solver = AStar(Manhattan())
    solver.run(puzzle, goal)


if __name__ == "__main__":
    main()
