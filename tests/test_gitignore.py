import tempfile
from pathlib import Path

import git

import easyconf


def test_git(mocker):
    with tempfile.TemporaryDirectory() as temp_dir:
        mocked_inspect = mocker.patch("easyconf.generators.gitignore.inspect")
        mocked_inspect.currentframe().f_back.f_back.f_code.co_filename = str(
            Path(temp_dir) / "settings.py"
        )
        git.Repo.init(temp_dir)
        path = Path(temp_dir)
        easyconf.Config(str(path / "example.yml"))
        assert (path / ".gitignore").exists()


def test_no_git(mocker):
    with tempfile.TemporaryDirectory() as temp_dir:
        mocked_inspect = mocker.patch("easyconf.generators.gitignore.inspect")
        mocked_inspect.currentframe().f_back.f_back.f_code.co_filename = str(
            Path(temp_dir) / "settings.py"
        )
        path = Path(temp_dir)
        easyconf.Config(str(path / "example.yml"))
        assert not (path / ".gitignore").exists()


def test_invalid_frame(mocker):
    with tempfile.TemporaryDirectory() as temp_dir:
        mocked_inspect = mocker.patch("easyconf.generators.gitignore.inspect")
        mocked_inspect.currentframe().f_back.f_back = None
        path = Path(temp_dir)
        easyconf.Config(str(path / "example.yml"))
        assert not (path / ".gitignore").exists()


def test_existing(mocker):
    with tempfile.TemporaryDirectory() as temp_dir:
        mocked_inspect = mocker.patch("easyconf.generators.gitignore.inspect")
        mocked_inspect.currentframe().f_back.f_back.f_code.co_filename = str(
            Path(temp_dir) / "settings.py"
        )
        git.Repo.init(temp_dir)
        path = Path(temp_dir)
        gitignore = path / ".gitignore"
        contents = "test\nexample.yml\nother\n"
        with open(gitignore, "w") as f:
            f.write(contents)
        easyconf.Config(str(path / "example.yml"))
        with open(gitignore, "r") as f:
            assert f.read() == contents


def test_existing_no_newline(mocker):
    with tempfile.TemporaryDirectory() as temp_dir:
        mocked_inspect = mocker.patch("easyconf.generators.gitignore.inspect")
        mocked_inspect.currentframe().f_back.f_back.f_code.co_filename = str(
            Path(temp_dir) / "settings.py"
        )
        git.Repo.init(temp_dir)
        path = Path(temp_dir)
        gitignore = path / ".gitignore"
        with open(gitignore, "w") as f:
            f.write("test")
        easyconf.Config(str(path / "example.yml"))
        with open(gitignore, "r") as f:
            assert f.read() == "test\nexample.yml\n"
