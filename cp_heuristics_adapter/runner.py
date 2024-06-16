import logging
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from time import perf_counter_ns
from typing import TextIO

from cp_heuristics_adapter.setup_logger import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


@dataclass
class RunResult:
    """Result of the run method.

    Attributes:
        output (str): Output of the program.
        returncode (int): Return code of the program.
        time_ms (float): Time [ms] taken by the program.
    """

    output: str
    time_ms: float

    def time_with_unit(self) -> str:
        """Return the time with the unit.

        Returns:
            str: Time with the unit.
        """
        return f"{self.time_ms:.0f} ms"


class ProgramRunner:
    """For running a program."""

    def __init__(self, exec_cmd: list[str]) -> None:
        """Initialize the ProgramRunner.

        Args:
            exec_cmd (list[str]): Command to execute the program (without arguments).
        """
        self.exec_cmd = exec_cmd
        assert self.exec_cmd
        # Replace ~ with the home directory
        if self.exec_cmd[0].startswith("~/"):
            self.exec_cmd[0] = str(Path.home() / self.exec_cmd[0][2:])

    def run(
        self,
        args: list[str],
        timeout: float | None = None,
        stdin: TextIO | None = None,
        stdout: TextIO | None = None,
        stderr: TextIO | None = None,
    ) -> RunResult:
        """Run the program.

        Args:
            args (list[str]): Arguments to pass to the program.
            timeout (float | None, optional): Timeout in seconds. Defaults to None.
            stdin (TextIO, optional): stdin (TextIO, optional). Defaults to None (sys.stdin).
            stdout (TextIO, optional): stdout (TextIO, optional). Defaults to None (sys.stdout).
            stderr (TextIO, optional): stderr (TextIO, optional). Defaults to None (sys.stderr).
        """
        if stdin is None:
            stdin = sys.stdin
        if stdout is None:
            stdout = sys.stdout
        if stderr is None:
            stderr = sys.stderr

        logger.info(f"running {self.exec_cmd + args}")
        start_time = perf_counter_ns()
        output = subprocess.check_output(
            args=self.exec_cmd + args,
            timeout=timeout,
            stdin=stdin,
            stderr=stderr,
            text=True,
        )
        end_time = perf_counter_ns()
        stdout.write(output)
        return RunResult(
            output=output,
            time_ms=(end_time - start_time) / 1_000_000,
        )


class Solver:
    """For running a solver program."""

    def __init__(self, name: str, runner: ProgramRunner) -> None:
        """Initialize the Solver.

        Args:
            name (str): Name of the solver.
            runner (ProgramRunner): ProgramRunner object.
        """
        self.name = name
        self.runner = runner

    def run(
        self,
        stdin: TextIO | None,
        stdout: TextIO | None,
        stderr: TextIO | None,
        timeout: float,
    ) -> RunResult:
        """Run the solver.

        Args:
            stdin (TextIO | None): stdin. None means sys.stdin.
            stdout (TextIO | None): stdout. None means sys.stdout.
            stderr (TextIO | None): stderr. None means sys.stderr.
            timeout (float): Timeout in seconds.
        """
        args: list[str] = []
        return self.runner.run(
            args=args, stdin=stdin, stdout=stdout, stderr=stderr, timeout=timeout
        )
