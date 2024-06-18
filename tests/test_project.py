from pathlib import Path

import pytest

from cp_heuristics_adapter.languages import Cpp, Language, Python
from cp_heuristics_adapter.project import Project


class TestProject:
    def test_root(self, sample_project_root: Path) -> None:
        project = Project(sample_project_root)
        assert project.root == sample_project_root

    def test_settings_dir(self, sample_project_root: Path) -> None:
        project = Project(sample_project_root)
        assert project.settings_dir == sample_project_root / ".cp-heuristics-adapter"

    def test_cpp_config_file(self, sample_project_root: Path) -> None:
        project = Project(sample_project_root)
        assert (
            project.cpp_config_file
            == sample_project_root / ".cp-heuristics-adapter" / "cpp_config.toml"
        )

    def test_python_config_file(self, sample_project_root: Path) -> None:
        project = Project(sample_project_root)
        assert (
            project.python_config_file
            == sample_project_root / ".cp-heuristics-adapter" / "py_config.toml"
        )

    @pytest.mark.parametrize("lang", [Cpp, Python])
    def test_config_file(self, lang: type[Language], sample_project_root: Path) -> None:
        project = Project(sample_project_root)
        config_file: Path
        if lang == Cpp:
            config_file = (
                sample_project_root / ".cp-heuristics-adapter" / "cpp_config.toml"
            )
        elif lang == Python:
            config_file = (
                sample_project_root / ".cp-heuristics-adapter" / "py_config.toml"
            )
        assert project.config_file(lang) == config_file

    def test_inputs_dir(self, sample_project_root: Path) -> None:
        project = Project(sample_project_root)
        assert project.inputs_dir == sample_project_root / "in"

    def test_outputs_dir(self, sample_project_root: Path) -> None:
        project = Project(sample_project_root)
        assert project.outputs_dir == sample_project_root / "out"

    @pytest.mark.parametrize("case_id", [0, 1, 10, 100, 9999])
    def test_input_file(self, case_id: int, sample_project_root: Path) -> None:
        project = Project(sample_project_root)
        filename: str
        if case_id == 0:
            filename = "0000.txt"
        elif case_id == 1:
            filename = "0001.txt"
        elif case_id == 10:
            filename = "0010.txt"
        elif case_id == 100:
            filename = "0100.txt"
        elif case_id == 9999:
            filename = "9999.txt"
        assert project.input_file(case_id) == sample_project_root / "in" / filename

    @pytest.mark.parametrize("case_id", [0, 1, 10, 100, 9999])
    def test_output_file(self, case_id: int, sample_project_root: Path) -> None:
        project = Project(sample_project_root)
        filename: str
        if case_id == 0:
            filename = "0000.txt"
        elif case_id == 1:
            filename = "0001.txt"
        elif case_id == 10:
            filename = "0010.txt"
        elif case_id == 100:
            filename = "0100.txt"
        elif case_id == 9999:
            filename = "9999.txt"
        assert project.output_file(case_id) == sample_project_root / "out" / filename

    def test_scores_dir(self, sample_project_root: Path) -> None:
        project = Project(sample_project_root)
        assert project.scores_dir == sample_project_root / "scores"

    @pytest.mark.parametrize("relative_path", ["", "dir", "dir/subdir"])
    def test_search_project_root(
        self, sample_project: Project, relative_path: Path
    ) -> None:
        assert (
            sample_project.search_project_root(sample_project.root / relative_path)
            == sample_project.root
        )

    @pytest.mark.parametrize("relative_path", ["", "dir", "dir/subdir"])
    def test_search_inner_project_root(
        self, sample_inner_project: Project, relative_path: Path
    ) -> None:
        assert (
            sample_inner_project.search_project_root(
                sample_inner_project.root / relative_path
            )
            == sample_inner_project.root
        )

    def test_search_project_root_not_found(self, sample_project: Project) -> None:
        with pytest.raises(FileNotFoundError):
            sample_project.search_project_root(sample_project.root.parent)

    def test_assert_empty(self, sample_project_root: Path) -> None:
        project = Project(sample_project_root)
        project.assert_empty()

    def test_assert_empty_with_ignorable_files(self, sample_project_root: Path) -> None:
        project = Project(sample_project_root)
        (project.root / "file").touch()
        (project.root / ".git").mkdir()
        project.assert_empty()

    @pytest.mark.parametrize(
        "dir_attr", ["settings_dir", "inputs_dir", "outputs_dir", "scores_dir"]
    )
    @pytest.mark.parametrize("file_type", ["file", "dir"])
    def test_assert_empty_not_empty(
        self, sample_project_root: Path, dir_attr: str, file_type: str
    ) -> None:
        project = Project(sample_project_root)
        child: Path = project.__dict__[dir_attr]
        if file_type == "file":
            child.touch()
        elif file_type == "dir":
            child.mkdir()
        with pytest.raises(FileExistsError):
            project.assert_empty()
