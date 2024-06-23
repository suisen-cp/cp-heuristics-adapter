import sys
from pathlib import Path
from typing import Generator, TextIO

import pytest
from pytest_mock import MockerFixture

from cp_heuristics_adapter.runner import (
    ProgramRunner,
    RunResult,
    Solver,
)


@pytest.fixture
def text_io_in(empty_dir: Path) -> Generator[TextIO, None, None]:
    file = empty_dir / "input.txt"
    file.touch()
    with file.open("r") as f:
        yield f


@pytest.fixture
def text_io_out(empty_dir: Path) -> Generator[TextIO, None, None]:
    file = empty_dir / "output.txt"
    with file.open("w") as f:
        yield f


@pytest.fixture
def text_io_err(empty_dir: Path) -> Generator[TextIO, None, None]:
    file = empty_dir / "error.txt"
    with file.open("w") as f:
        yield f


class TestRunResult:
    @pytest.mark.parametrize(
        "time_ms, expected",
        [
            (0, "0 ms"),
            (123.4, "123 ms"),
            (1000.0, "1000 ms"),
        ],
    )
    def test_time_with_unit(self, time_ms: float, expected: str) -> None:
        result = RunResult(output="", time_ms=time_ms)
        assert result.time_with_unit() == expected


class TestProgramRunner:
    @pytest.mark.parametrize(
        "exec_cmd, expected",
        [
            (["~/foo"], [str(Path.home() / "foo")]),
            (["/usr/bin/echo"], ["/usr/bin/echo"]),
            (["python"], ["python"]),
        ],
    )
    def test_init(self, exec_cmd: list[str], expected: list[str]) -> None:
        runner = ProgramRunner(exec_cmd)
        assert runner.exec_cmd == expected

    def test_init_empty(self) -> None:
        with pytest.raises(AssertionError):
            ProgramRunner([])

    @pytest.mark.parametrize(
        "stdin, stdout, stderr, timeout",
        [
            (None, None, None, 2.0),
            (sys.stdin, sys.stdout, sys.stderr, None),
        ],
    )
    def test_run_std_inout(
        self,
        mocker: MockerFixture,
        stdin: TextIO | None,
        stdout: TextIO | None,
        stderr: TextIO | None,
        timeout: float | None,
    ) -> None:
        exec_cmd = ["python", "hoge.py"]
        args = ["arg1", "arg2"]

        runner = ProgramRunner(exec_cmd=exec_cmd)
        check_output_mock = mocker.patch(
            "subprocess.check_output", return_value="hello"
        )

        result = runner.run(
            args=args, timeout=timeout, stdin=stdin, stdout=stdout, stderr=stderr
        )
        assert result.output == "hello"
        assert result.time_ms > 0
        check_output_mock.assert_called_once_with(
            args=["python", "hoge.py", "arg1", "arg2"],
            timeout=timeout,
            stdin=sys.stdin,
            stderr=sys.stderr,
            text=True,
        )

    def test_run_custom_inout(
        self,
        mocker: MockerFixture,
        text_io_in: TextIO,
        text_io_out: TextIO,
        text_io_err: TextIO,
    ) -> None:
        exec_cmd = ["python", "hoge.py"]
        args = ["arg1", "arg2"]

        runner = ProgramRunner(exec_cmd=exec_cmd)
        check_output_mock = mocker.patch(
            "subprocess.check_output", return_value="hello"
        )

        result = runner.run(
            args=args,
            timeout=None,
            stdin=text_io_in,
            stdout=text_io_out,
            stderr=text_io_err,
        )
        assert result.output == "hello"
        assert result.time_ms > 0
        check_output_mock.assert_called_once_with(
            args=["python", "hoge.py", "arg1", "arg2"],
            timeout=None,
            stdin=text_io_in,
            stderr=text_io_err,
            text=True,
        )


class TestSolver:
    @pytest.fixture
    def runner(self) -> ProgramRunner:
        return ProgramRunner(["python", "solver.py"])

    def test_init(self, runner: ProgramRunner) -> None:
        solver = Solver("solver", runner)
        assert solver.name == "solver"
        assert solver.runner == runner

    def test_run_std_inout(self, runner: ProgramRunner, mocker: MockerFixture) -> None:
        run_mock = mocker.patch("cp_heuristics_adapter.runner.ProgramRunner.run")
        solver = Solver("solver", runner)
        solver.run(
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr,
            timeout=2.0,
        )
        run_mock.assert_called_once_with(
            args=[],
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr,
            timeout=2.0,
        )

    def test_run_custom_inout(
        self,
        runner: ProgramRunner,
        mocker: MockerFixture,
        text_io_in: TextIO,
        text_io_out: TextIO,
        text_io_err: TextIO,
    ) -> None:
        run_mock = mocker.patch("cp_heuristics_adapter.runner.ProgramRunner.run")
        solver = Solver("solver", runner)
        solver.run(
            stdin=text_io_in,
            stdout=text_io_out,
            stderr=text_io_err,
            timeout=10.0,
        )
        run_mock.assert_called_once_with(
            args=[],
            stdin=text_io_in,
            stdout=text_io_out,
            stderr=text_io_err,
            timeout=10.0,
        )
