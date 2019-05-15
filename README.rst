========
EasyConf
========

Easy file-based and environment configuration.

Usage
=====

First create a ``Config`` object:

.. code:: python

    config = easyconf.Config('config.yaml')

Then reference a configuration variable as an attribute of this object:

.. code:: python

    some_variable = config.SOME_VARIABLE()

At runtime, EasyConf will try to each variable from the following sources
in order:

1. A matching environment variable

2. A matching variable within the configuration file

3. The ``default`` attribute (if no attribute is provided, an
   ``easyconf.config.RequiredConfigVarMissing`` exception will be raised)

Config file generation
----------------------

If the ``Config`` file doesn't exist yet and the file location is writable,
EasyConf will generate it using the ``initial`` values and commented
``default`` values defined in each configuration variable.

Don't hide configuration variables within conditional statements, load them at
the top of a module so they can be generated regardless.


Example Django configuration
============================

.. code:: python

    import easyconf

    config = easyconf.Config('myproject.yaml')

    DEBUG = config.DEBUG(default=False)
    DATABASES = {'default': config.DATABASE(
        default='postgres:///myproject',
        cast=easyconf.dict_or_url,
    )}
    SECRET_KEY = config.SECRET_KEY(initial=easyconf.random_text_generator(60))


Configuration Variable options
==============================

``default``
    The default value for the variable if it is not provided in the environment
    or in the configuration file.

``initial``
    A value or callable used to set the initial value of a variable in the
    configuration file.

``help``
    Help text to use in the configuration file for this variable.

``cast``
    A callable to convert an incoming value (from the environment or
    configuration file) to the correct Python type.


``Config`` Object options
=========================

``default_files``
    A file or list of files to attempt to read configuration variables from. If
    multiple files are provided, only the first one found will be used.

    If none of the provided files are found, the first one in a writable
    location will be created and populated automatically.

``file_env_var``
    An environment variable which could be used to specify the configuration
    file path.

    If provided and an environment variable matches, this overrides any
    ``default_files`` specified.


Helper Modules
==============

``easyconf.dict_or_url``
------------------------

Expand url strings defined in django-environ_ into dictionaries. For example:

.. code:: pycon

    >>> import easyconf
    >>> easyconf.dict_or_url('mysql:///abc')
    {'NAME': 'abc', 'USER': '', 'PASSWORD': '', 'HOST': '', 'PORT': '', 'ENGINE': 'django.db.backends.mysql'}

.. _django-environ: https://pypi.org/project/django-environ/

``easyconf.random_text_generator``
----------------------------------

Creates a function that can be called to securely generate a random text string
of a predefined length (containing base64 characters).

Useful for the ``initial`` configuration variable option.

.. code:: pycon

    >>> import easyconf
    >>> gen = easyconf.random_text_generator(20)
    >>> gen()
    'sYw0D/7xjXqxfCyUdHqr'
    >>> gen()
    'ig1Z1n+mFLt+qYNOmD6I'
