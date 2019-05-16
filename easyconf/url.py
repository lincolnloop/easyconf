from environ import Env
from urllib.parse import urlparse


scheme_map = {}
for attr, method in [
    ("DB_SCHEMES", "db_url_config"),
    ("CACHE_SCHEMES", "cache_url_config"),
    ("EMAIL_SCHEMES", "email_url_config"),
    ("SEARCH_SCHEMES", "search_url_config"),
]:
    method = getattr(Env, method)
    for scheme in getattr(Env, attr):
        scheme_map[scheme] = method


def url_to_dict(url):
    if url == "sqlite://:memory:":
        url = url.replace(":memory:", "")
    url = urlparse(url)
    if url.scheme not in scheme_map:
        raise RuntimeError(f"Unknown url scheme: {url.scheme}")
    return scheme_map[url.scheme](url)


def dict_or_url(url):
    if isinstance(url, dict):
        return url
    return url_to_dict(url)


dict_or_url.cast_from_config = True
