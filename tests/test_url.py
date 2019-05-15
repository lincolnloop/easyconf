import pytest

from easyconf.url import url_to_dict, dict_or_url


def test_bad_url():
    with pytest.raises(RuntimeError):
        url_to_dict("ftp://test")


def test_database_url():
    assert url_to_dict("mysql://abc:1234") == {
        "ENGINE": "django.db.backends.mysql",
        "HOST": "abc",
        "NAME": "",
        "PASSWORD": "",
        "PORT": 1234,
        "USER": "",
    }


def test_database_memory_url():
    assert url_to_dict("sqlite://:memory:") == {
        "ENGINE": "django.db.backends.sqlite3",
        "HOST": "",
        "NAME": ":memory:",
        "PASSWORD": "",
        "PORT": "",
        "USER": "",
    }


def test_cache_url():
    assert url_to_dict("filecache:///var/cache/test") == {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": "/var/cache/test",
    }


def test_email_url():
    assert url_to_dict("smtp+tls://smtp.gmail.com") == {
        "EMAIL_BACKEND": "django.core.mail.backends.smtp.EmailBackend",
        "EMAIL_FILE_PATH": "",
        "EMAIL_HOST": "smtp.gmail.com",
        "EMAIL_HOST_PASSWORD": None,
        "EMAIL_HOST_USER": None,
        "EMAIL_PORT": None,
        "EMAIL_USE_TLS": True,
    }


def test_search_url():
    assert url_to_dict("solr://solr:4321") == {
        "ENGINE": "haystack.backends.solr_backend.SolrEngine",
        "URL": "http://solr:4321",
    }


def test_dict_or_url_dict():
    d = {"Already": "dict"}
    assert dict_or_url(d) == d


def test_dict_or_url_url():
    assert dict_or_url("dummycache://") == {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        "LOCATION": "",
    }
