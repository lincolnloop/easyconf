import logging
import os.path
import tempfile
from pathlib import Path

import pytest

import easyconf
from easyconf.config import RequiredConfigVarMissing

EXAMPLE_CONF = str(Path(__file__).parent / "example.yaml")


def test_find_any_existing():
    with tempfile.TemporaryDirectory() as temp_dir:
        nonexistant = str(Path(temp_dir) / "example.yml")
        config = easyconf.Config([nonexistant, EXAMPLE_CONF])
        assert config.BANANAS() == 1


def test_make_first():
    with tempfile.TemporaryDirectory() as temp_dir:
        bad = str(Path(temp_dir) / "bad" / "example.yml")
        good = str(Path(temp_dir) / "example.yml")
        following = str(Path(temp_dir) / "example2.yml")
        config = easyconf.Config([bad, good])
        config.CHOCOLATE(initial="yum")
        assert os.path.exists(good)
        assert not os.path.exists(bad)
        assert not os.path.exists(following)


def test_cant_make(caplog):
    logging.getLogger().info("test")
    with tempfile.TemporaryDirectory() as temp_dir:
        bad = str(Path(temp_dir) / "bad" / "example.yml")
        config = easyconf.Config(bad)
        assert config.TEST(default=1) == 1

        logged = [record[1:] for record in caplog.record_tuples]
        assert logged == [
            (
                logging.WARNING,
                "No configuration files found, attempting to create one...",
            ),
            (logging.WARNING, "Could not create a configuration file"),
        ]


def test_initial():
    with tempfile.TemporaryDirectory() as temp_dir:
        path = str(Path(temp_dir) / "example.yml")
        config = easyconf.Config(path)
        assert config.CHOCOLATE(initial="yum") == "yum"
        with open(path) as f:
            assert f.read() == "CHOCOLATE: yum\n"


def test_initial_with_help():
    with tempfile.TemporaryDirectory() as temp_dir:
        path = str(Path(temp_dir) / "example.yml")
        config = easyconf.Config(path)
        assert config.CHOCOLATE(initial="yum", help="Chocolate preference") == "yum"
        with open(path) as f:
            assert f.read() == "# Chocolate preference\nCHOCOLATE: yum\n"


def test_default():
    with tempfile.TemporaryDirectory() as temp_dir:
        path = str(Path(temp_dir) / "example.yml")
        config = easyconf.Config(path)
        assert config.CHOCOLATE(default="yum") == "yum"
        assert config.APPLES(default=0) == 0
        with open(path) as f:
            assert (
                f.read()
                == """\
# CHOCOLATE: yum

# APPLES: 0
{}
"""
            )


def test_required_var():
    with tempfile.TemporaryDirectory() as temp_dir:
        path = str(Path(temp_dir) / "example.yml")
        config = easyconf.Config(path)
        with pytest.raises(RequiredConfigVarMissing):
            config.CHOCOLATE()


def test_default_with_help():
    with tempfile.TemporaryDirectory() as temp_dir:
        path = str(Path(temp_dir) / "example.yml")
        config = easyconf.Config(path)
        config.CHOCOLATE(default="yum", help="Chocolate preference")
        with open(path) as f:
            assert f.read() == "# Chocolate preference\n# CHOCOLATE: yum\n{}\n"


def test_multiple():
    with tempfile.TemporaryDirectory() as temp_dir:
        path = str(Path(temp_dir) / "example.yml")
        config = easyconf.Config(path)
        assert config.FIRST(default="1") == "1"
        assert config.SECOND(initial="2", help="Second") == "2"
        assert config.THIRD(default="3", help="third") == "3"
        assert config.FOURTH(initial=lambda: "four") == "four"
        assert config.FIFTH(default="5") == "5"
        assert config.LAST(default="end") == "end"
        with open(path) as f:
            assert (
                f.read()
                == """\
# FIRST: '1'

# Second
SECOND: '2'

# third
# THIRD: '3'

FOURTH: four

# FIFTH: '5'

# LAST: end
"""
            )


def test_disabled():
    with tempfile.TemporaryDirectory() as temp_dir:
        nonexistant = str(Path(temp_dir) / "example.yml")
        config = easyconf.Config(nonexistant, generate=False)
        assert config.APPLES(default=1) == 1
        assert not os.path.exists(nonexistant)


def test_cast():
    with tempfile.TemporaryDirectory() as temp_dir:
        path = str(Path(temp_dir) / "example.yml")
        config = easyconf.Config(path)
        assert config.CASTED(default="1", cast=lambda x: {"inner": int(x)}) == {
            "inner": 1
        }
        with open(path) as f:
            assert (
                f.read()
                == """\
# CASTED:
#   inner: 1
{}
"""
            )
