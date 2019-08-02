==========
Change Log
==========

1.3 (2019-08-02)
================

- Use environment values for automatic configuration generation.


1.2.2 (2019-08-02)
==================

- Correctly lock down ``ruamel.yaml`` this time (it's v0.16, not v16).


1.2.1 (2019-08-01)
==================

- Avoid new version of ``ruamel.yaml`` which changed loading format.


1.2 (2019-05-21)
================

- When generating a config that is within a git repository, add it to
  ``.gitignore``.

- If a cast callable has a ``cast_from_config`` attribute set to ``True``, cast
  values coming from the configuration file. This is set to ``True`` for the
  ``dict_or_url`` helper method.


1.1.1 (2019-05-16)
==================

- Fix issue with generating multiple comments (for multiple default values) at
  the end of the YAML config.

- Cast default values when writing to config.


1.1 (2019-05-15)
================

- Allow explicit disabling of automatic config generation.

- Cast default values if a ``cast`` argument is provided.


1.0 (2019-05-15)
================

- Initial Release
