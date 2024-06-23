import shutil
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Generator

import pytest

from cp_heuristics_adapter.project import Project


@pytest.fixture
def empty_dir() -> Generator[Path, None, None]:
    with TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def sample_project_root() -> Generator[Path, None, None]:
    with TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def sample_inner_project_root(sample_project_root: Path) -> Generator[Path, None, None]:
    with TemporaryDirectory(dir=sample_project_root) as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def sample_project(sample_project_root: Path) -> Project:
    project = Project(sample_project_root)
    project.settings_dir.mkdir(parents=False, exist_ok=False)
    project.cpp_config_file.touch()
    project.python_config_file.touch()
    project.inputs_dir.mkdir(parents=False, exist_ok=False)
    project.outputs_dir.mkdir(parents=False, exist_ok=False)
    project.scores_dir.mkdir(parents=False, exist_ok=False)
    return project


@pytest.fixture
def sample_inner_project(sample_inner_project_root: Path) -> Project:
    project = Project(sample_inner_project_root)
    project.settings_dir.mkdir(parents=False, exist_ok=False)
    project.cpp_config_file.touch()
    project.python_config_file.touch()
    project.inputs_dir.mkdir(parents=False, exist_ok=False)
    project.outputs_dir.mkdir(parents=False, exist_ok=False)
    project.scores_dir.mkdir(parents=False, exist_ok=False)
    return project


@pytest.fixture
def cpp_config_toml() -> Generator[Path, None, None]:
    source = Path(__file__).parent / "data" / "cpp_config.toml"
    with TemporaryDirectory() as temp_dir:
        dest = Path(temp_dir) / "cpp_config.toml"
        shutil.copy(source, dest)
        yield dest


@pytest.fixture
def py_config_toml() -> Generator[Path, None, None]:
    source = Path(__file__).parent / "data" / "py_config.toml"
    with TemporaryDirectory() as temp_dir:
        dest = Path(temp_dir) / "py_config.toml"
        shutil.copy(source, dest)
        yield dest
