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
      - |github-action| |requires| |coveralls|
    * - package
      - |version| |supported-versions| |supported-implementations|

.. |docs| image:: http://readthedocs.org/projects/autodocsumm/badge/?version=latest
    :alt: Documentation Status
    :target: http://autodocsumm.readthedocs.io/en/latest/?badge=latest

.. |github-action| image:: https://github.com/Chilipp/autodocsumm/workflows/Tests/badge.svg
    :alt: Tests
    :target: https://github.com/Chilipp/autodocsumm/actions?query=workflow%3A%22Tests%22

.. |coveralls| image:: https://coveralls.io/repos/github/Chilipp/autodocsumm/badge.svg?branch=master
    :alt: Coverage
    :target: https://coveralls.io/github/Chilipp/autodocsumm?branch=master

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

Or you install it via::

    $ python setup.py install

from the `source on GitHub`_.


.. _source on GitHub: https://github.com/Chilipp/autodocsumm


Requirements
============
The package only requires Sphinx_ to be installed. It has been tested for
versions higher than 1.3.


.. _Sphinx: http://www.sphinx-doc.org/en/stable


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
