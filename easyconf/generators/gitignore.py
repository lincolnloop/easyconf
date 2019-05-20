import inspect
from pathlib import Path

import git


def update_gitignore(path: str, frames: int = 2) -> None:
    parent_frame = inspect.currentframe()
    for i in range(frames):
        parent_frame = parent_frame.f_back
        if not parent_frame:
            return
    parent_path = Path(parent_frame.f_code.co_filename).resolve().parent

    # Get the git root.
    try:
        git_path = Path(
            git.Repo(str(parent_path), search_parent_directories=True).working_tree_dir
        )
    except git.InvalidGitRepositoryError:
        return

    # Get the relative path compared to the git root.
    try:
        relative_path = Path(path).resolve().relative_to(git_path)
    except ValueError:
        # Path not within git root.
        return

    # Append to the gitignore
    with open(git_path.joinpath(".gitignore"), "a+b") as f:
        f.seek(0)
        lines = f.readlines()
        new_line = f"{relative_path}\n".encode("utf-8")
        if new_line in lines:
            # Ignore line already exists
            return
        # Ensure we start on a new line.
        if lines and lines[-1][-1] != b"\n":
            f.write(b"\n")
        f.write(new_line)
