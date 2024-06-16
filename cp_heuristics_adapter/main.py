import argparse
import logging
import sys

from cp_heuristics_adapter.setup_logger import setup_logging
from cp_heuristics_adapter.subcommands.clean import Clean
from cp_heuristics_adapter.subcommands.init import Init
from cp_heuristics_adapter.subcommands.run import Run

setup_logging()
logger = logging.getLogger(__name__)

if logger.level != logging.DEBUG:
    # Disable traceback in case of error
    sys.tracebacklimit = 0

# Mapping of subcommand classes to their names
subcommand_names: dict[type, str] = {
    Init: "init",
    Run: "run",
    Clean: "clean",
}


def main() -> None:
    """Entry point of the program."""
    parser = argparse.ArgumentParser(prog="cp-heuristics-adapter")
    subparsers = parser.add_subparsers(dest="subcommand")

    subcommand_init = Init(
        subparsers,
        name=subcommand_names[Init],
        description="Initialize a new project",
    )
    subcommand_init.add_arguments()

    subcommand_run = Run(
        subparsers,
        name=subcommand_names[Run],
        description="Run the program",
    )
    subcommand_run.add_arguments()

    subcommand_clean = Clean(
        subparsers,
        name=subcommand_names[Clean],
        description="Clean the project",
    )
    subcommand_clean.add_arguments()

    args = parser.parse_args()
    subcommand: str = args.subcommand
    logger.debug(f"Running subcommand: {subcommand}")

    if subcommand == subcommand_names[Init]:
        try:
            subcommand_init.run(args)
        except Exception:
            logger.exception("An error occurred while running the 'init' subcommand")
    elif subcommand == subcommand_names[Run]:
        try:
            subcommand_run.run(args)
        except Exception:
            logger.exception("An error occurred while running the 'run' subcommand")
    elif subcommand == subcommand_names[Clean]:
        try:
            subcommand_clean.run(args)
        except Exception:
            logger.exception("An error occurred while running the 'clean' subcommand")
    else:
        parser.print_help()
