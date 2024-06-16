import shutil
from pathlib import Path


def delete_if_allowed(file_path: Path) -> bool:
    """Try to delete a file or a folder interactively.

    Args:
        file_path (Path): The path to the file or folder to be deleted.
    Returns:
        bool: True if the file or folder was deleted, False otherwise.
    """
    if not file_path.exists():
        return True
    file_type = "file" if file_path.is_file() else "folder"
    while True:
        print(
            f'Is it ok to remove the {file_type} "{file_path.resolve()}"? [y/n]: ',
            end="",
            flush=True,
        )
        response = input().strip().lower()
        if response in ["yes", "y"]:
            if file_path.is_file():
                file_path.unlink()
            else:
                shutil.rmtree(file_path)
            return True
        elif response in ["no", "n"]:
            return False
