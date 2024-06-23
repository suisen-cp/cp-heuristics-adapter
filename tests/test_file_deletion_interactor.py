from pathlib import Path

import pytest
from pytest_mock import MockerFixture

from cp_heuristics_adapter.util.file_deletion_interactor import delete_if_allowed

YES_PATTERNS = [
    pytest.param(["yes"], id="yes"),
    pytest.param(["YES"], id="YES"),
    pytest.param(["a", "yes"], id="yes after invalid input"),
    pytest.param(["a", "YES"], id="YES after invalid input"),
    pytest.param(["yes\n"], id="yes with newline"),
    pytest.param(["YES\n"], id="yes with newline"),
    pytest.param([" yes "], id="yes with spaces before and after"),
    pytest.param([" YES "], id="YES with spaces before and after"),
    pytest.param(["y"], id="y"),
    pytest.param(["Y"], id="Y"),
    pytest.param(["a", "y"], id="y after invalid input"),
    pytest.param(["a", "Y"], id="Y after invalid input"),
    pytest.param(["y\n"], id="y with newline"),
    pytest.param(["Y\n"], id="Y with newline"),
    pytest.param([" y "], id="y with spaces before and after"),
    pytest.param([" Y "], id="Y with spaces before and after"),
]

NO_PATTERNS = [
    pytest.param(["no"], id="no"),
    pytest.param(["NO"], id="NO"),
    pytest.param(["a", "no"], id="no after invalid input"),
    pytest.param(["a", "NO"], id="NO after invalid input"),
    pytest.param(["no\n"], id="no with newline"),
    pytest.param(["NO\n"], id="NO with newline"),
    pytest.param([" no "], id="no with spaces before and after"),
    pytest.param([" NO "], id="NO with spaces before and after"),
    pytest.param(["n"], id="n"),
    pytest.param(["N"], id="N"),
    pytest.param(["a", "n"], id="n after invalid input"),
    pytest.param(["a", "N"], id="N after invalid input"),
    pytest.param(["n\n"], id="n with newline"),
    pytest.param(["N\n"], id="N with newline"),
    pytest.param([" n "], id="n with spaces before and after"),
    pytest.param([" N "], id="N with spaces before and after"),
]


class TestFileDeletionInteractor:
    @pytest.mark.parametrize("input_values", YES_PATTERNS)
    def test_delete_if_allowed_yes(
        self, mocker: MockerFixture, empty_dir: Path, input_values: list[str]
    ) -> None:
        mocker.patch("builtins.input", side_effect=input_values)

        file = empty_dir / "file.txt"
        file.touch()
        assert delete_if_allowed(file)
        assert not file.exists()

    @pytest.mark.parametrize("input_values", NO_PATTERNS)
    def test_delete_if_allowed_no(
        self, mocker: MockerFixture, empty_dir: Path, input_values: list[str]
    ) -> None:
        mocker.patch("builtins.input", side_effect=input_values)

        file = empty_dir / "file.txt"
        file.touch()
        assert not delete_if_allowed(file)
        assert file.exists()

    def test_delete_if_allowed_existing_file_yes(
        self, mocker: MockerFixture, empty_dir: Path
    ) -> None:
        mocker.patch("builtins.input", side_effect=["y"])

        file = empty_dir / "file.txt"
        file.touch()
        assert delete_if_allowed(file)
        assert not file.exists()

    def test_delete_if_allowed_existing_file_no(
        self, mocker: MockerFixture, empty_dir: Path
    ) -> None:
        mocker.patch("builtins.input", side_effect=["n"])

        file = empty_dir / "file.txt"
        file.touch()
        assert not delete_if_allowed(file)
        assert file.exists()

    def test_delete_if_allowed_existing_folder_yes(
        self, mocker: MockerFixture, empty_dir: Path
    ) -> None:
        mocker.patch("builtins.input", side_effect=["y"])

        folder = empty_dir / "folder"
        folder.mkdir()
        assert delete_if_allowed(folder)
        assert not folder.exists()

    def test_delete_if_allowed_existing_nonempty_folder_yes(
        self, mocker: MockerFixture, empty_dir: Path
    ) -> None:
        mocker.patch("builtins.input", side_effect=["y"])

        folder = empty_dir / "folder"
        folder.mkdir()
        (folder / "file.txt").touch()
        assert delete_if_allowed(folder)
        assert not folder.exists()

    def test_delete_if_allowed_existing_folder_no(
        self, mocker: MockerFixture, empty_dir: Path
    ) -> None:
        mocker.patch("builtins.input", side_effect=["n"])

        folder = empty_dir / "folder"
        folder.mkdir()
        assert not delete_if_allowed(folder)
        assert folder.exists()

    def test_delete_if_allowed_non_existing_file(
        self, mocker: MockerFixture, empty_dir: Path
    ) -> None:
        mocker.patch(
            "builtins.input",
            side_effect=Exception("`input` must not be called in this case."),
        )
        file = empty_dir / "non_existent"
        assert delete_if_allowed(file)
        assert not file.exists()
