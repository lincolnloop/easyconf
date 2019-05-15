from pathlib import Path

import pytest

import easyconf
from easyconf.config import RequiredConfigVarMissing

EXAMPLE_CONF = str(Path(__file__).parent / "example.yaml")
EXAMPLE_JSON_CONF = str(Path(__file__).parent / "example.json")


def test_env(monkeypatch):
    monkeypatch.setenv("TEST", "True")
    assert easyconf.Config().TEST() == "True"


def test_env_cast_from_default(monkeypatch):
    monkeypatch.setenv("APPLES", "2")
    assert easyconf.Config().APPLES(default=1) == 2


def test_env_list(monkeypatch):
    monkeypatch.setenv("FRUIT", "Apples,Bananas")
    assert easyconf.Config().FRUIT(cast=list) == ["Apples", "Bananas"]


def test_env_bool(monkeypatch):
    monkeypatch.setenv("TEST", "False")
    assert easyconf.Config().TEST(cast=bool) is False


def test_conf_file(monkeypatch):
    config = easyconf.Config(EXAMPLE_CONF)
    assert config.BANANAS() == 1
    assert config.APPLES() is None
    monkeypatch.setenv("APPLES", "ten")
    assert config.APPLES() == "ten"


def test_conf_file_from_json(monkeypatch):
    config = easyconf.Config(EXAMPLE_JSON_CONF)
    assert config.BANANAS() == 2
    assert config.APPLES() == "three"
    monkeypatch.setenv("APPLES", "ten")
    assert config.APPLES() == "ten"


def test_conf_file_from_env(monkeypatch):
    monkeypatch.setenv("CONF_FILE", EXAMPLE_CONF)
    config = easyconf.Config(file_env_var="CONF_FILE")
    assert config.BANANAS() == 1


def test_required_var():
    config = easyconf.Config(EXAMPLE_CONF)
    with pytest.raises(RequiredConfigVarMissing):
        config.CHOCOLATE()


def test_default_var():
    config = easyconf.Config(EXAMPLE_CONF)
    assert config.BANANAS(default=2) == 1
    assert config.CHOCOLATE(default="yum") == "yum"


def test_initial_var():
    config = easyconf.Config(EXAMPLE_CONF)
    assert config.BANANAS(initial=2) == 1


def test_cast(monkeypatch):
    monkeypatch.setenv("APPLES", "1")
    assert easyconf.Config().APPLES(cast=int) == 1


def test_cast_default():
    assert easyconf.Config().APPLES(default="1", cast=int) == 1
