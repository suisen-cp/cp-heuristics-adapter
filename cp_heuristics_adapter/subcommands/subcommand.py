from __future__ import annotations

import argparse
from abc import ABCMeta, abstractmethod


class Subcommand(metaclass=ABCMeta):
    """Subcommand."""

    def __init__(
        self,
        subparser: argparse._SubParsersAction[argparse.ArgumentParser],
        name: str,
        description: str,
    ):
        """Initialize the Subcommand.

        Args:
            subparser (argparse._SubParsersAction): Subparser.
            name (str): Name of the subcommand.
            description (str): Description of the subcommand.
        """
        self.parser = subparser.add_parser(name=name, description=description)

    @abstractmethod
    def add_arguments(self) -> None:
        """Add arguments to the parser."""
        pass

    @abstractmethod
    def run(self, raw_args: argparse.Namespace) -> None:
        """Run the subcommand.

        Args:
            raw_args (argparse.Namespace): Raw arguments.
        """
        pass
