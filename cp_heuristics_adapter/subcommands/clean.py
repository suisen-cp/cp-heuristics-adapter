import argparse
import logging
from dataclasses import dataclass
from pathlib import Path

from cp_heuristics_adapter.project import Project
from cp_heuristics_adapter.setup_logger import setup_logging
from cp_heuristics_adapter.subcommands.subcommand import Subcommand
from cp_heuristics_adapter.util.file_deletion_interactor import delete_if_allowed

setup_logging()
logger = logging.getLogger(__name__)


class Clean(Subcommand):
    """Clean the project."""

    @dataclass(frozen=True)
    class Args:
        """Arguments for the clean subcommand.

        Attributes:
            path (Path): Path to the project directory.
        """

        path: Path

    def add_arguments(self) -> None:
        """Add arguments to the parser."""
        self.parser.add_argument(
            "-p", "--path", type=str, default=".", help="Path to project directory"
        )

    def parse_args(self, args: argparse.Namespace) -> "Clean.Args":
        """Parse the arguments.

        Args:
            args (argparse.Namespace): Arguments.

        Returns:
            Clean.Args: Parsed arguments.
        """
        path = Path(args.path).expanduser()
        return Clean.Args(path=path)

    def run(self, raw_args: argparse.Namespace) -> None:
        """Run the subcommand.

        Args:
            raw_args (argparse.Namespace): Raw arguments.
        """
        args = self.parse_args(raw_args)
        logger.debug(f"Running subcommand 'clean' with args: {args}")
        project_root = args.path

        project = Project(project_root)

        logger.info(f"Cleaning project at {project_root.resolve()}")
        delete_if_allowed(project.settings_dir)
        delete_if_allowed(project.inputs_dir)
        delete_if_allowed(project.outputs_dir)
        delete_if_allowed(project.scores_dir)

        logger.info("Project cleaned successfully")
