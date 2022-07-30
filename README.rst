==============================================
Extending your autodoc API docs with a summary
==============================================

.. start-badges

.. list-table::
    :stub-columns: 1
    :widths: 10 90

    * - docs
      - |docs|
    * - tests
      - |github-action| |requires| |codecov|
    * - package
      - |version| |supported-versions| |supported-implementations|

.. |docs| image:: http://readthedocs.org/projects/autodocsumm/badge/?version=latest
    :alt: Documentation Status
    :target: http://autodocsumm.readthedocs.io/en/latest/?badge=latest

.. |github-action| image:: https://github.com/Chilipp/autodocsumm/workflows/Tests/badge.svg
    :alt: Tests
    :target: https://github.com/Chilipp/autodocsumm/actions?query=workflow%3A%22Tests%22

.. |codecov| image:: https://codecov.io/gh/Chilipp/autodocsumm/branch/master/graph/badge.svg?token=I9wlZyhI4Y
    :alt: Codecov
    :target: https://codecov.io/gh/Chilipp/autodocsumm

.. |requires| image:: https://requires.io/github/Chilipp/autodocsumm/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/Chilipp/autodocsumm/requirements/?branch=master

.. |version| image:: https://img.shields.io/pypi/v/autodocsumm.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/autodocsumm

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/autodocsumm.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/autodocsumm

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/autodocsumm.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/autodocsumm


.. end-badges

Welcome! This sphinx extension provides some useful extensions to the Sphinxs
autodoc_ extension. Those are

1. It creates a *Table of Contents* in the style of the autosummary_ extension
   with methods, classes, functions and attributes
2. As you can include the ``__init__`` method documentation for via the
   autoclass_content_ configuration value,
   we provide the *autodata_content* configuration value to include
   the documentation from the ``__call__`` method
3. You can exclude the string representation of specific objects. E.g. if you
   have a large dictionary using the *not_document_data* configuration
   value.

See the `Documentation on Readthedocs`_ for more details.

.. _autodoc: http://www.sphinx-doc.org/en/stable/ext/autodoc.html
.. _autoclass_content: http://www.sphinx-doc.org/en/stable/ext/autodoc.html#confval-autoclass_content
.. _autosummary: http://www.sphinx-doc.org/en/stable/ext/autosummary.html
.. _Documentation on Readthedocs: http://autodocsumm.readthedocs.io/en/latest/



Installation
============
Simply install it via ``pip``::

    $ pip install autodocsumm


Local development
^^^^^^^^^^^^^^^^^

Use ``pip`` on the `source on GitHub`_::

    $ pip install .


.. _source on GitHub: https://github.com/Chilipp/autodocsumm


Requirements
============
The package only requires Sphinx_ to be installed. It has been tested for
versions higher than 1.3.


.. _Sphinx: http://www.sphinx-doc.org/en/master


Quickstart
==========

In order to activate the autodocsumm extension, you have to list it in your
``conf.py``:

.. code-block:: python

    extensions = [
        'sphinx.ext.autodoc',
        ...,
        'autodocsumm',
    ]

Once this is done, you can use the ``:autosummary:`` option for autodoc
directives to generate a table at the top, e.g.:

.. code-block:: rst

    .. automodule:: my.awesome.module
        :autosummary:

Optionally, you can make autodocsumm active by default for all autodoc
directives by adding in ``conf.py``:

.. code-block:: python

    autodoc_default_options = {
        'autosummary': True,
    }


Disclaimer
==========
Copyright 2016-2019, Philipp S. Sommer

Copyright 2020-2021, Helmholtz-Zentrum Hereon

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
