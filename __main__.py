import argparse

__CHECK_PERF = False
if __CHECK_PERF:
    import cProfile
    import pstats

from npuzzle.benchmark import Benchmark
from npuzzle.distance import AVAILABLE_HEURISTICS, DEFAULT_HEURISTIC, Distance
from npuzzle.npuzzle import MAX_N_VALUE, MIN_N_VALUE, Npuzzle
from npuzzle.solver import AVAILABLE_SOLVERS, DEFAULT_SOLVER, Solver


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
        puzzle = Npuzzle.from_random(args.random, solvable=not args.unsolvable)

    # check if the puzzle is solvable
    if not puzzle.is_solvable():
        print(f"This puzzle can't be solved.\n{puzzle}")
        return

    # get the heuristic
    heuristic = args.heuristic()

    # get the solver
    solver = args.solver(heuristic)

    print(
        f"For:\n{puzzle}\nRunning with {type(solver).__name__} and {type(heuristic).__name__}...\n"
    )

    # run
    if __CHECK_PERF:
        profile = cProfile.Profile()
        res = profile.runcall(solver.run, puzzle, puzzle.goal)
        ps = pstats.Stats(profile)
        ps.print_stats()
    else:
        res = solver.run(puzzle, puzzle.goal)

    # print the report
    if res is None:
        print("No solution found.")
    else:
        try:
            res.display_genealogy(ascending=False)
        except RecursionError:
            print("The path is too big to be displayed.")
        finally:
            print(solver.report)


def get_args() -> argparse.Namespace:
    """Get the arguments from command line."""

    def check_random(value: str) -> int:
        """Check the size of the puzzle."""

        if MIN_N_VALUE <= int(value) <= MAX_N_VALUE:
            return int(value)
        else:
            raise argparse.ArgumentTypeError(
                f"The value of 'random' must be in ({MIN_N_VALUE}, {MAX_N_VALUE}) range. ({value} here)"
            )

    def check_heuristic(value: str) -> Distance:
        """Check the value of solver."""

        for heuristic in AVAILABLE_HEURISTICS:
            if heuristic.__name__ == value:
                return heuristic
        raise argparse.ArgumentTypeError(
            f"The value of 'heuristic' must be in {([heuristic.__name__ for heuristic in AVAILABLE_HEURISTICS])}. ({value!r} here)"  # type: ignore
        )

    def check_solver(value: str) -> Solver:
        """Check the value of solver."""

        for solver in AVAILABLE_SOLVERS:
            if solver.__name__ == value:
                return solver
        raise argparse.ArgumentTypeError(
            f"The value of 'solver' must be in {([solver.__name__ for solver in AVAILABLE_SOLVERS])}. ({value!r} here)"  # type: ignore
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
        type=check_random,
        metavar="N",
        default=3,
        help="generate a random N puzzle",
    )
    parser.add_argument(
        "-he",
        "--heuristic",
        type=check_heuristic,
        metavar="NAME",
        default=DEFAULT_HEURISTIC,
        help="particular way of calculating the distance",
    )
    parser.add_argument(
        "-s",
        "--solver",
        type=check_solver,
        metavar="NAME",
        default=DEFAULT_SOLVER,
        help="the algorithm to use",
    )
    parser.add_argument(
        "-u",
        "--unsolvable",
        action="store_true",
        default=False,
        help="Forces generation of an unsolvable puzzle. Ignored when -f ",
    )

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = get_args()

    puzzle = Npuzzle.from_random(args.random, solvable=not args.unsolvable)
    benchmark = Benchmark(AVAILABLE_SOLVERS, AVAILABLE_HEURISTICS)
    # benchmark = Benchmark([DEFAULT_SOLVER], AVAILABLE_HEURISTICS)
    reports = benchmark.run(puzzle, puzzle.goal)
    for report in reports:
        print(report)
    benchmark.display(reports)

    # main(args)
