import logging
from pathlib import Path

from cp_heuristics_adapter.languages import Cpp, Language, Python
from cp_heuristics_adapter.setup_logger import setup_logging
from cp_heuristics_adapter.util.pathlib_util import assert_not_exists


setup_logging()
logger = logging.getLogger(__name__)


class Project:
    """Represents a project directory."""

    def __init__(self, root: Path) -> None:
        """Initialize the Project.

        Args:
            root (Path): Path to the project directory.
        """
        self.root = root
        self.settings_dir = root / ".cp-heuristics-adapter"
        self.cpp_config_file = self.settings_dir / "cpp_config.toml"
        self.python_config_file = self.settings_dir / "py_config.toml"
        self.inputs_dir = self.root / "in"
        self.outputs_dir = self.root / "out"
        self.scores_dir = self.root / "scores"

    def input_file(self, case_id: int) -> Path:
        """Get the input file for the case.

        Args:
            case_id (int): Case ID.

        Returns:
            Path: Path to the input file.
        """
        return self.inputs_dir / f"{case_id:04}.txt"

    def output_file(self, case_id: int) -> Path:
        """Get the output file for the case.

        Args:
            case_id (int): Case ID.

        Returns:
            Path: Path to the output file.
        """
        return self.outputs_dir / f"{case_id:04}.txt"

    @staticmethod
    def search_project_root(path: Path) -> Path:
        """Search for the project root directory.

        Args:
            path (Path): Path to start searching from.

        Raises:
            FileNotFoundError: If the project root directory is not found.

        Returns:
            Path: Path to the project root directory.
        """
        while True:
            if (path / ".cp-heuristics-adapter").exists():
                return path
            if path == path.parent:
                raise FileNotFoundError(".cp-heuristics-adapter directory not found")
            path = path.parent

    def assert_empty(self) -> None:
        """Assert that the project directory is empty."""
        assert_not_exists(self.settings_dir)
        assert_not_exists(self.inputs_dir)
        assert_not_exists(self.outputs_dir)
        assert_not_exists(self.scores_dir)

    def config_file(self, lang: type[Language]) -> Path:
        """Get the config file for the language.

        Args:
            lang (type[Language]): Language.

        Returns:
            Path: Path to the config file.
        """
        config_file_map = {
            Cpp: self.cpp_config_file,
            Python: self.python_config_file,
        }
        return config_file_map[lang]
