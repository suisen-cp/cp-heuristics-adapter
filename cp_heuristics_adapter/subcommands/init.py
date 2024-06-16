import argparse
from dataclasses import dataclass
import logging
from pathlib import Path
import shutil
from cp_heuristics_adapter.project import Project
from cp_heuristics_adapter.setup_logger import setup_logging
from cp_heuristics_adapter.subcommands.subcommand import Subcommand
from cp_heuristics_adapter.util.file_deletion_interactor import delete_if_allowed

setup_logging()
logger = logging.getLogger(__name__)


class Init(Subcommand):
    """Initialize a new project.

    Attributes:
        TEMPLATES_DIR (Path): Path to the templates directory.
    """

    TEMPLATES_DIR = Path(__file__).parent.parent.parent / "templates"

    @dataclass(frozen=True)
    class Args:
        """Arguments for the init subcommand.

        Attributes:
            path (Path): Path to the project directory.
            overwrite (bool): Whether to overwrite existing files.
        """

        path: Path
        overwrite: bool

    def add_arguments(self) -> None:
        """Add arguments to the parser.

        path: Path to the project directory
        overwrite: Whether to overwrite existing files
        """
        self.parser.add_argument(
            "-p", "--path", type=str, default=".", help="Path to project directory"
        )
        self.parser.add_argument(
            "--overwrite", action="store_true", help="Overwrite existing files"
        )

    def parse_args(self, args: argparse.Namespace) -> "Init.Args":
        """Parse the arguments.

        Args:
            args (argparse.Namespace): Arguments.

        Returns:
            Init.Args: Parsed arguments.
        """
        path = Path(args.path).expanduser()
        overwrite: bool = args.overwrite
        return Init.Args(path=path, overwrite=overwrite)

    def run(self, raw_args: argparse.Namespace) -> None:
        """Run the subcommand.

        Args:
            raw_args (argparse.Namespace): Raw arguments.

        Raises:
            FileExistsError: If the project directory is not empty and --overwrite is not specified.
        """
        args = self.parse_args(raw_args)
        logger.debug(f"Running subcommand 'init' with args: {args}")
        project_root = args.path
        overwrite = args.overwrite

        project = Project(project_root)

        if not overwrite:
            logger.info(f"Checking if {project_root.resolve()} is empty")
            try:
                project.assert_empty()
            except FileExistsError as e:
                logger.error(e)
                logger.error("Use --overwrite to overwrite existing files")
                raise e
        else:
            logger.info(f"Overwriting {project_root.resolve()}")

        logger.info(f"Initializing project at {project_root.resolve()}")

        project.inputs_dir.mkdir(parents=True, exist_ok=True)
        project.outputs_dir.mkdir(parents=True, exist_ok=True)
        project.scores_dir.mkdir(parents=True, exist_ok=True)
        project.settings_dir.mkdir(parents=True, exist_ok=True)

        logger.info("Copying template config files")
        template_project = Project(Init.TEMPLATES_DIR)
        for template_config_file in template_project.settings_dir.iterdir():
            config_file = project.settings_dir / template_config_file.name
            if not config_file.exists() or delete_if_allowed(config_file):
                shutil.copy(template_config_file, config_file)

        logger.info("Project initialized successfully")
