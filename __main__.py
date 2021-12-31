from npuzzle.npuzzle import Npuzzle, Move

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
        res = puzzle.make_move(move)

def main() -> None:
    """Main function."""

    test_make_move(5)


if __name__ == "__main__":
    main()
