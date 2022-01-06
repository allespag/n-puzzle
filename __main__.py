import argparse

from npuzzle.distance import AVAILABLE_HEURISTICS, DEFAULT_HEURISTIC
from npuzzle.npuzzle import Npuzzle
from npuzzle.solver import AVAILABLE_SOLVERS, DEFAULT_SOLVER


def main(args: argparse.Namespace) -> None:
    """Main function."""

    # generate the puzzle
    if args.file:
        try:
            puzzle = Npuzzle.from_file(args.file)
        except Exception as e:
            print(f"Error: {e}")
            return
    else:
        puzzle = Npuzzle.from_random(args.random)

    # check if the puzzle is solvable
    if not puzzle.solvable:
        print(f"This puzzle can't be solved.\n{puzzle}")
        return

    # choose a heuristic evaluator
    heuristic = next(
        filter(lambda h: h.__name__ == args.heuristic, AVAILABLE_HEURISTICS),
        DEFAULT_HEURISTIC,
    )()

    # choose a solver
    solver = next(
        filter(lambda s: s.__name__ == args.solver, AVAILABLE_SOLVERS),
        DEFAULT_SOLVER,
    )(heuristic)

    print(
        f"Run with {type(solver).__name__} and {type(heuristic).__name__} for: \n{puzzle}\n"
    )
    res = solver.run(puzzle, puzzle.goal)

    # print path
    if res is None:
        print("No solution found.")
    else:
        res.display_genealogy(ascending=False)


def get_args() -> argparse.Namespace:
    """Get the arguments from command line."""

    def check_heuristic(value: str) -> str:
        """Check the value of heuristic."""

        AVAILABLE_HEURISTICS_str = [h.__name__ for h in AVAILABLE_HEURISTICS]
        if value in AVAILABLE_HEURISTICS_str:
            return value
        else:
            raise argparse.ArgumentTypeError(
                f"The value of 'heuristic' must be in {AVAILABLE_HEURISTICS_str}. ({value} here)"
            )

    def check_solver(value: str) -> str:
        """Check the value of solver."""

        AVAILABLE_SOLVERS_str = [s.__name__ for s in AVAILABLE_SOLVERS]
        if value in AVAILABLE_SOLVERS_str:
            return value
        else:
            raise argparse.ArgumentTypeError(
                f"The value of 'solver' must be in {AVAILABLE_SOLVERS_str}. ({value} here)"
            )

    parser = argparse.ArgumentParser(prog="n-puzzle")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-f",
        "--file",
        type=str,
        metavar="FILENAME",
        help="n-puzzle to load",
    )
    group.add_argument(
        "-r",
        "--random",
        type=int,
        metavar="N",
        default=3,
        help="generate a random N puzzle",
    )
    parser.add_argument(
        "-he",
        "--heuristic",
        type=check_heuristic,
        metavar="NAME",
        default=DEFAULT_HEURISTIC.__name__,
        help="particular way of calculating the distance",
    )
    parser.add_argument(
        "-s",
        "--solver",
        type=check_solver,
        metavar="NAME",
        default=DEFAULT_SOLVER.__name__,
        help="the algorithm to use",
    )

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = get_args()
    main(args)
