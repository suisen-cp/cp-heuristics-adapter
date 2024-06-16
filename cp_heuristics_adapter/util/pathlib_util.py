from pathlib import Path


def assert_dir_existence(path: Path) -> None:
    """Assert the directory exists.

    Args:
        path (Path): Path to the directory.

    Raises:
        FileNotFoundError: If the directory does not exist.
    """
    if not path.is_dir():
        raise FileNotFoundError(f"Directory '{path}' not found.")


def assert_file_existence(path: Path) -> None:
    """Assert the file exists.

    Args:
        path (Path): Path to the file.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    if not path.is_file():
        raise FileNotFoundError(f"File '{path}' not found.")


def assert_not_exists(path: Path) -> None:
    """Assert the file/directory does not exist.

    Args:
        path (Path): Path to the file/directory.

    Raises:
        FileExistsError: If the file/directory exists.
    """
    if path.exists():
        raise FileExistsError(f"File/Directory '{path}' already exists.")


def assert_empty_dir(path: Path) -> None:
    """Assert the directory is empty.

    Args:
        path (Path): Path to the directory.

    Raises:
        FileExistsError: If the directory is not empty.
    """
    if not path.is_dir() or [*path.iterdir()]:
        raise FileExistsError(f"Directory '{path}' is not empty.")
