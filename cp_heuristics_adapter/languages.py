import logging
import subprocess
from abc import ABCMeta, abstractmethod
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Any

import toml

from cp_heuristics_adapter.runner import ProgramRunner
from cp_heuristics_adapter.setup_logger import setup_logging
from cp_heuristics_adapter.util import pathlib_util
from cp_heuristics_adapter.util.config_util import ConfigKey

setup_logging()
logger = logging.getLogger(__name__)


class BuildMode(Enum):
    """Build mode.

    DEBUG: Debug mode.
    RELEASE: Release mode.
    """

    DEBUG = "debug"
    RELEASE = "release"

    @staticmethod
    def from_str(value: str) -> "BuildMode":
        """Get the BuildMode from the value.

        Args:
            value (str): Value.

        Raises:
            ValueError: If the value is invalid.

        Returns:
            BuildMode: BuildMode.
        """
        for mode in BuildMode:
            if mode.value == value:
                return mode
        raise ValueError(f"Invalid mode: {value}")


class Language(metaclass=ABCMeta):
    @abstractmethod
    def __init__(
        self, *, build_mode: BuildMode, config_file: Path | None = None
    ) -> None:
        """Set up the language.

        Args:
            build_mode (BuildMode): Build mode.
            config_file (Path | None, optional): Path to the config file. Defaults to None.
        """
        pass

    @lru_cache
    @abstractmethod
    def compile(self, source_file: Path) -> ProgramRunner:
        """Compile the source file if necessary.

        Args:
            source_file (Path): Path to the source file.

        Returns:
            ProgramRunner: ProgramRunner object.
        """
        pass

    @classmethod
    @abstractmethod
    def suffixes(self) -> list[str]:
        """Get the suffixes of the source files.

        Returns:
            list[str]: List of suffixes.
        """
        pass


class Cpp(Language):
    """Cpp language class."""

    class Config:
        """Cpp configuration class.

        Attributes:
            COMPILER (ConfigKey[str]): Compiler. Defaults to "g++".
            FLAGS (ConfigKey[list[str]]): Compilation flags. Defaults to ["-O2", "-Wall", "-Wextra"].
        """

        COMPILER = ConfigKey[str](
            key="compiler",
            default="g++",
        )
        FLAGS = ConfigKey[list[str]](
            key="flags",
            default=[
                "-O2",
                "-Wall",
                "-Wextra",
            ],
        )

        def __init__(
            self, *, build_mode: BuildMode, config_file: Path | None = None
        ) -> None:
            """Initialize the Cpp config.

            Args:
                build_mode (BuildMode): Build mode.
                config_file (Path | None, optional): Path to the config file. Defaults to None.
            """
            config: dict[str, Any] = {}
            if config_file is not None:
                logger.info(f"loading cpp config from {config_file}")
                pathlib_util.assert_file_existence(config_file)
                config = toml.load(config_file)[build_mode.value]
            else:
                logger.info("using default cpp config")
            self.compiler = Cpp.Config.COMPILER.load_from(config)
            self.flags = Cpp.Config.FLAGS.load_from(config)

            logger.debug(f"compiler: {self.compiler}")
            logger.debug(f"flags: {self.flags}")

    def __init__(
        self, *, build_mode: BuildMode, config_file: Path | None = None
    ) -> None:
        """Initialize the Cpp object.

        You can customize the compiler and compilation flags by providing a config file.

        Args:
            build_mode (BuildMode): Build mode.
            config_file (Path | None, optional): Path to the config file. Defaults to None.
        """
        self.config = Cpp.Config(build_mode=build_mode, config_file=config_file)

    @lru_cache
    def compile(self, source_file: Path) -> ProgramRunner:
        """Compile the source file.

        Args:
            source_file (Path): Path to the source file.

        Returns:
            ProgramRunner: ProgramRunner object.
        """
        exec_file = source_file.with_suffix("")

        compile_cmd = [self.config.compiler]
        compile_cmd.extend(self.config.flags)
        compile_cmd.extend([str(source_file), "-o", str(exec_file)])

        logger.info(f"compiling {source_file} with {compile_cmd}")
        subprocess.check_call(compile_cmd)

        return ProgramRunner([f"./{exec_file}"])

    @classmethod
    def suffixes(self) -> list[str]:
        return [".cpp", ".cc", ".cxx"]


class Python(Language):
    """Python language class."""

    class Config:
        """Python configuration class.

        Attributes:
            PYTHON (ConfigKey[str]): Python command. Defaults to "python".
        """

        PYTHON = ConfigKey[str](
            key="python",
            default="python",
        )

        def __init__(
            self, *, build_mode: BuildMode, config_file: Path | None = None
        ) -> None:
            """Initialize the Python config.

            Args:
                build_mode (BuildMode): Build mode.
                config_file (Path | None, optional): Path to the config file. Defaults to None.
            """
            config: dict[str, Any] = {}
            if config_file is not None:
                logger.info(f"loading python config from {config_file}")
                pathlib_util.assert_file_existence(config_file)
                config = toml.load(config_file)[build_mode.value]
            else:
                logger.info("using default python config")
            self.python = Python.Config.PYTHON.load_from(config)

    def __init__(
        self, *, build_mode: BuildMode, config_file: Path | None = None
    ) -> None:
        """Initialize the Python object.

        You can customize the python command by providing a config file.

        Args:
            build_mode (BuildMode): Build mode.
            config_file (Path | None, optional): Path to the config file. Defaults to None.
        """
        self.config = Python.Config(build_mode=build_mode, config_file=config_file)

    @lru_cache
    def compile(self, source_file: Path) -> ProgramRunner:
        """Python does not need compilation, so this method just returns a ProgramRunner object.

        Args:
            source_file (Path): Path to the source file.

        Returns:
            ProgramRunner: ProgramRunner object.
        """
        logger.info("compilation is not needed for python")
        return ProgramRunner([self.config.python, str(source_file)])

    @classmethod
    def suffixes(self) -> list[str]:
        return [".py"]


def detect_language(source_file: Path) -> type[Language]:
    """Detect the language of the source file.

    Args:
        source_file (Path): Path to the source file.

    Returns:
        type[Language]: Language class.
    """
    langs: list[type[Language]] = [Cpp, Python]
    for lang in langs:
        if source_file.suffix in lang.suffixes():
            return lang
    raise ValueError(f"Unsupported language: {source_file.suffix}")
