import argparse
import datetime
import logging
import math
import statistics
import subprocess
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from tempfile import NamedTemporaryFile

from cp_heuristics_adapter.languages import BuildMode, detect_language
from cp_heuristics_adapter.project import Project
from cp_heuristics_adapter.runner import ProgramRunner
from cp_heuristics_adapter.setup_logger import setup_logging
from cp_heuristics_adapter.subcommands.subcommand import Subcommand

setup_logging()
logger = logging.getLogger(__name__)


class ScoreType(Enum):
    """Type of score.

    PLAIN: Plain score.
    LOG: Logarithm of the score.
    """

    PLAIN = "plain"
    LOG = "log"

    @staticmethod
    def from_str(value: str) -> "ScoreType":
        """Get the ScoreType from the value.

        Args:
            value (str): Value.

        Raises:
            ValueError: If the value is invalid.

        Returns:
            ScoreType: ScoreType.
        """
        for score_type in ScoreType:
            if score_type.value == value:
                return score_type
        raise ValueError(f"Invalid score type: {value}")


class ScoreSummary:
    """Summary of scores."""

    def __init__(self, scores: list[int] | list[float]) -> None:
        """Initialize the ScoreSummary.

        Args:
            scores (list[int] | list[float]): Scores.
        """
        self.count = len(scores)
        self.sum = sum(scores)
        self.min = min(scores)
        self.max = max(scores)
        self.mean = statistics.mean(scores)
        self.median = statistics.median(scores)
        self.stdev = statistics.stdev(scores)

    def pretty(self) -> str:
        """Return the summary in a pretty format.

        Returns:
            str: Summary in a pretty format.
        """
        return (
            f"count: {self.count}\n"
            f"sum  : {self.sum:.2f}\n"
            f"min  : {self.min:.2f}\n"
            f"max  : {self.max:.2f}\n"
            f"mean : {self.mean:.2f}\n"
            f"med  : {self.median:.2f}\n"
            f"stdev: {self.stdev:.2f}\n"
        )


class Run(Subcommand):
    """Subcommand 'run'.

    Run the program with the given input and output files.

    Attributes:
        DEFAULT_MODE (BuildMode): Default build mode.
        DEFAULT_TIME_LIMIT (float): Default time limit.
        DEFAULT_SCORE_TYPE (ScoreType): Default score type.
    """

    DEFAULT_MODE = BuildMode.DEBUG
    DEFAULT_TIME_LIMIT = 2.0
    DEFAULT_SCORE_TYPE = ScoreType.PLAIN

    @dataclass(frozen=True)
    class Args:
        """Arguments for the 'run' subcommand.

        Attributes:
            source (Path): Path to source file.
            number (int): Number of cases to run.
            build_mode (BuildMode): Build mode.
            timelimit (float): Time limit for execution.
            score_type (ScoreType): Type of score.
        """

        source: Path
        number: int
        build_mode: BuildMode
        timelimit: float
        score_type: ScoreType

    def add_arguments(self) -> None:
        """Add arguments.

        source: Path to source file.
        number: Number of cases to run.
        build-mode: Build mode.
        time-limit: Time limit for execution.
        score-type: Type of score.
        """
        self.parser.add_argument(
            "source",
            type=str,
            help="Path to source file.",
        )
        self.parser.add_argument(
            "number",
            type=int,
            help="Number of cases to run.",
        )
        self.parser.add_argument(
            "-b",
            "--build-mode",
            type=str,
            choices=[mode.value for mode in BuildMode],
            default=Run.DEFAULT_MODE.value,
            help=f"Build mode. Default is '{Run.DEFAULT_MODE.value}'.",
        )
        self.parser.add_argument(
            "-t",
            "--time-limit",
            type=float,
            default=Run.DEFAULT_TIME_LIMIT,
            help=f"Time limit for execution. Default is {Run.DEFAULT_TIME_LIMIT:.1f} seconds.",
        )
        self.parser.add_argument(
            "-s",
            "--score-type",
            type=str,
            choices=[score_type.value for score_type in ScoreType],
            default=Run.DEFAULT_SCORE_TYPE.value,
            help=(
                "Type of score. "
                "If a standings is calculated by the relative score, "
                f"it is recommended to use '{ScoreType.LOG.value}' type. "
                f"Default is '{Run.DEFAULT_SCORE_TYPE.value}'."
            ),
        )

    def parse_args(self, args: argparse.Namespace) -> "Run.Args":
        """Parse the arguments.

        Args:
            args (argparse.Namespace): Arguments.

        Returns:
            Run.Args: Parsed arguments.
        """
        source = Path(args.source).expanduser()
        number: int = args.number
        build_mode = BuildMode.from_str(args.build_mode)
        timelimit: float = args.time_limit
        score_type = ScoreType.from_str(args.score_type)
        return Run.Args(
            source=source,
            number=number,
            build_mode=build_mode,
            timelimit=timelimit,
            score_type=score_type,
        )

    def __run_single_case(
        self,
        *,
        input_file: Path,
        output_file: Path,
        timelimit: float,
        runner: ProgramRunner,
    ) -> int:
        """Run a single case.

        Args:
            input_file (Path): Path to the input file.
            output_file (Path): Path to the output file.
            timelimit (float): Time limit.
            runner (ProgramRunner): Program runner.

        Raises:
            CalledProcessError: If a runtime error occurs.
            TimeoutExpired: If the time limit is exceeded.

        Returns:
            int: Score.
        """
        logger.info(f"Running {input_file.name}")
        with (
            NamedTemporaryFile(mode="w") as tmpf,
            input_file.open("r") as inf,
            output_file.open("w") as ouf,
        ):
            solver_args = [tmpf.name]
            try:
                runner.run(
                    args=solver_args,
                    timeout=timelimit,
                    stdin=inf,
                    stdout=ouf,
                )
            except subprocess.CalledProcessError as e:
                logger.error("Runtime error occured")
                raise e
            except subprocess.TimeoutExpired as e:
                logger.error("Time limit exceeded")
                raise e
            with open(tmpf.name, "r") as in_tmpf:
                score = int(in_tmpf.read())
        return score

    def __run_all_cases(
        self,
        *,
        project: Project,
        runner: ProgramRunner,
        number: int,
        timelimit: float,
    ) -> list[int]:
        """Run all cases.

        Args:
            project (Project): Project.
            runner (ProgramRunner): Program runner.
            number (int): Number of cases.
            timelimit (float): Time limit.

        Returns:
            list[int]: Scores.
        """
        scores = [
            self.__run_single_case(
                input_file=project.input_file(case_id),
                output_file=project.output_file(case_id),
                timelimit=timelimit,
                runner=runner,
            )
            for case_id in range(number)
        ]
        return scores

    def __write_scores(self, scores: list[int], scores_file: Path) -> None:
        """Write scores to a file.

        Args:
            scores (list[int]): Scores.
            scores_file (Path): Path to the scores file.
        """
        with scores_file.open("w") as f:
            for score in scores:
                f.write(f"{score}\n")

    def __write_scores_sum(
        self, score_summary: ScoreSummary, scores_sum_file: Path
    ) -> None:
        """Write scores summary to a file.

        Args:
            score_summary (ScoreSummary): Score summary.
            scores_sum_file (Path): Path to the scores summary file.
        """
        with scores_sum_file.open("w") as f:
            f.write(f"{score_summary.pretty()}")

    def run(self, raw_args: argparse.Namespace) -> None:
        """Run the subcommand.

        Args:
            raw_args (argparse.Namespace): Raw arguments.
        """
        args = self.parse_args(raw_args)
        logger.debug(f"Running subcommand 'run' with args: {args}")
        project_root = Project.search_project_root(args.source)
        project = Project(project_root)

        logger.info("Detecting the language of the source file")
        Lang = detect_language(args.source)
        logger.info(f"Detected language: {Lang.__name__}")
        source_language = Lang(
            build_mode=args.build_mode, config_file=project.config_file(Lang)
        )

        logger.info("Building the source file")
        runner = source_language.compile(args.source)

        logger.info(f"Running {args.number} cases")
        scores = self.__run_all_cases(
            project=project,
            runner=runner,
            number=args.number,
            timelimit=args.timelimit,
        )

        logger.info("Writing scores")
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        scores_file = project.scores_dir / f"scores_{timestamp}.txt"
        self.__write_scores(scores, scores_file)

        logger.info("Writing scores summary")
        scores_processed: list[int] | list[float]
        if args.score_type == ScoreType.LOG:
            scores_processed = [math.log(score) for score in scores]
        else:
            scores_processed = scores
        scores_sum_file = project.scores_dir / f"scores_{timestamp}.summary.txt"
        self.__write_scores_sum(ScoreSummary(scores_processed), scores_sum_file)

        logger.info("All done successfully")
