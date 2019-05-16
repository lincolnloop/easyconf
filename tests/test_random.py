from easyconf.random import random_text_generator


def test_generator(monkeypatch):
    monkeypatch.setattr("os.urandom", lambda len: b"notrandom"[:len])

    assert random_text_generator(4)() == "bm90"
    assert random_text_generator(5)() == "bm90c"


def test_different():
    generator = random_text_generator(10)
    assert generator() != generator()
