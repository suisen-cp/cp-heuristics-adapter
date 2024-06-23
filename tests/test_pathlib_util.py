from pathlib import Path

import pytest

from cp_heuristics_adapter.util.pathlib_util import (
    assert_dir_existence,
    assert_empty_dir,
    assert_file_existence,
    assert_not_exists,
)


class TestPathlibUtil:
    def test_assert_dir_existence(self, empty_dir: Path) -> None:
        assert_dir_existence(empty_dir)

    def test_assert_dir_existence_non_existing(self, empty_dir: Path) -> None:
        child = empty_dir / "child"
        with pytest.raises(FileNotFoundError):
            assert_dir_existence(child)

    def test_assert_dir_existence_file(self, empty_dir: Path) -> None:
        child = empty_dir / "child"
        child.touch()
        with pytest.raises(FileNotFoundError):
            assert_dir_existence(child)

    def test_assert_file_existence(self, empty_dir: Path) -> None:
        child = empty_dir / "child"
        child.touch()
        assert_file_existence(child)

    def test_assert_file_existence_non_existing(self, empty_dir: Path) -> None:
        child = empty_dir / "child"
        with pytest.raises(FileNotFoundError):
            assert_file_existence(child)

    def test_assert_file_existence_dir(self, empty_dir: Path) -> None:
        child = empty_dir / "child"
        child.mkdir()
        with pytest.raises(FileNotFoundError):
            assert_file_existence(child)

    def test_assert_not_exists(self, empty_dir: Path) -> None:
        child = empty_dir / "child"
        assert_not_exists(child)

    def test_assert_not_exists_existing(self, empty_dir: Path) -> None:
        child = empty_dir / "child"
        child.touch()
        with pytest.raises(FileExistsError):
            assert_not_exists(child)

    def test_assert_empty_dir(self, empty_dir: Path) -> None:
        assert_empty_dir(empty_dir)

    def test_assert_empty_dir_existing_file(self, empty_dir: Path) -> None:
        child = empty_dir / "child"
        child.touch()
        with pytest.raises(FileExistsError):
            assert_empty_dir(empty_dir)

    def test_assert_empty_dir_existing_dir(self, empty_dir: Path) -> None:
        child = empty_dir / "child"
        child.mkdir()
        with pytest.raises(FileExistsError):
            assert_empty_dir(empty_dir)
