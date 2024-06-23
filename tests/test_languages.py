from pathlib import Path

import pytest
from pytest_mock import MockerFixture

from cp_heuristics_adapter.languages import (
    BuildMode,
    Cpp,
    Language,
    Python,
    detect_language,
)


class TestBuildMode:
    def test_build_mode_from_str_debug(self) -> None:
        assert BuildMode.from_str("debug") == BuildMode.DEBUG

    def test_build_mode_from_str_release(self) -> None:
        assert BuildMode.from_str("release") == BuildMode.RELEASE

    def test_build_mode_from_str_invalid(self) -> None:
        with pytest.raises(ValueError):
            BuildMode.from_str("hoge")


class TestCpp:
    def test_cpp_config_debug(self, cpp_config_toml: Path) -> None:
        config = Cpp.Config(build_mode=BuildMode.DEBUG, config_file=cpp_config_toml)
        assert config.compiler == "g++"
        assert config.flags == [
            "-g",
            "-fsanitize=address",
            "-fsanitize=undefined",
            "-Wall",
            "-Wextra",
        ]

    def test_cpp_config_release(self, cpp_config_toml: Path) -> None:
        config = Cpp.Config(build_mode=BuildMode.RELEASE, config_file=cpp_config_toml)
        assert config.compiler == "clang++"
        assert config.flags == [
            "-O2",
            "-Wall",
            "-Wextra",
            "-Werror",
        ]

    @pytest.mark.parametrize(
        "build_mode",
        [
            BuildMode.DEBUG,
            BuildMode.RELEASE,
        ],
    )
    def test_no_config(self, mocker: MockerFixture, build_mode: BuildMode) -> None:
        mocker.patch("toml.load", side_effect=FileNotFoundError)
        config = Cpp.Config(build_mode=build_mode, config_file=None)
        assert config.compiler == "g++"
        assert config.flags == ["-O2", "-Wall", "-Wextra"]

    def test_cpp_config_not_found(self, empty_dir: Path) -> None:
        config_file = empty_dir / "hoge.toml"
        with pytest.raises(FileNotFoundError):
            Cpp.Config(build_mode=BuildMode.DEBUG, config_file=config_file)

    class DummyCppConfig:
        def __init__(
            self, *, build_mode: BuildMode, config_file: Path | None = None
        ) -> None:
            self.compiler = "g++"
            self.flags = ["-O2", "-Wall", "-Wextra", "-Werror"]

    def test_compile(self, mocker: MockerFixture) -> None:
        mocker.patch(
            "cp_heuristics_adapter.languages.Cpp.Config", new=self.DummyCppConfig
        )
        mock_compile = mocker.patch("subprocess.check_call")
        mock_runner = mocker.patch("cp_heuristics_adapter.languages.ProgramRunner")

        cpp = Cpp(build_mode=BuildMode.RELEASE, config_file=Path("dummy.toml"))
        source_file = Path("a/b/c.cpp")
        cpp.compile(source_file)

        mock_compile.assert_called_once_with(
            [
                "g++",
                "-O2",
                "-Wall",
                "-Wextra",
                "-Werror",
                str(Path("a/b/c.cpp")),
                "-o",
                str(Path("a/b/c")),
            ]
        )
        mock_runner.assert_called_once_with(["./a/b/c"])


class TestPython:
    def test_py_config_debug(self, py_config_toml: Path) -> None:
        config = Python.Config(build_mode=BuildMode.DEBUG, config_file=py_config_toml)
        assert config.python == "~/.pyenv/shims/python"

    def test_py_config_release(self, py_config_toml: Path) -> None:
        config = Python.Config(build_mode=BuildMode.RELEASE, config_file=py_config_toml)
        assert config.python == "python"

    @pytest.mark.parametrize(
        "build_mode",
        [
            BuildMode.DEBUG,
            BuildMode.RELEASE,
        ],
    )
    def test_no_config(self, mocker: MockerFixture, build_mode: BuildMode) -> None:
        mocker.patch("toml.load", side_effect=FileNotFoundError)
        config = Python.Config(build_mode=build_mode, config_file=None)
        assert config.python == "python"

    def test_py_config_not_found(self, empty_dir: Path) -> None:
        config_file = empty_dir / "hoge.toml"
        with pytest.raises(FileNotFoundError):
            Cpp.Config(build_mode=BuildMode.DEBUG, config_file=config_file)

    class DummyPythonConfig:
        def __init__(
            self, *, build_mode: BuildMode, config_file: Path | None = None
        ) -> None:
            self.python = "python3"

    def test_compile(self, mocker: MockerFixture) -> None:
        mocker.patch(
            "cp_heuristics_adapter.languages.Python.Config", new=self.DummyPythonConfig
        )
        mock_runner = mocker.patch("cp_heuristics_adapter.languages.ProgramRunner")

        python = Python(build_mode=BuildMode.RELEASE, config_file=Path("dummy.toml"))
        source_file = Path("a/b/c.py")
        python.compile(source_file)

        mock_runner.assert_called_once_with(["python3", str(Path("a/b/c.py"))])


@pytest.mark.parametrize(
    "file, lang",
    [
        (Path("a/b/c.cpp"), Cpp),
        (Path("a/b/c.cc"), Cpp),
        (Path("a/b/c.cxx"), Cpp),
        (Path("a/b/c.py"), Python),
    ],
)
def test_detect_language(file: Path, lang: type[Language]) -> None:
    assert detect_language(file) == lang


def test_detect_language_unknown() -> None:
    with pytest.raises(ValueError):
        detect_language(Path("a/b/c.hoge"))
