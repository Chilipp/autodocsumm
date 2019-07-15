.. highlight:: rest

Configuration of the sphinx extension
=====================================

The module provides 3 additional configuration values, one event and new
flags for the autodoc directives :rst:dir:`autoclass` and :rst:dir:`automodule`.

.. _autodoc-flags:

Additional flags for autodoc directives
---------------------------------------
The most important new flag for the :rst:dir:`autoclass` and
:rst:dir:`automodule` directives is the ``autosummary`` flag. If you want to
have an automatically generated summary to your class or module, you have to
add this flag, e.g. via::

    .. autodoc:: MyClass
        :autosummary:

or in the :confval:`autodoc_default_options` configuration value of sphinx
via

.. code-block:: python

    autodoc_default_options = {'autosummary': True}

See also the :ref:`examples` section it's usage.

The other additional flags let you control what should be in the autosummary
table: these are

- ``autosummary-private-members``
- ``autosummary-undoc-members``
- ``autosummary-inherited-members``
- ``autosummary-special-members``
- ``autosummary-exlude-members``
- ``autosummary-imported-members``
- ``autosummary-ignore-module-all``
- ``autosummary-members``

They are essentially the same as the options for :mod:`~sphinx.ext.autodoc`
(i.e. ``private-members`` or ``members``, but they only affect the
autosummary table (see the example in :ref:`summary-table-example`).


.. _confvals:

Configuration values and events
-------------------------------

.. event:: autodocsumm-grouper (app, what, name, obj, section, parent)

    Emitted when autodocsumm has to determine the section for a member in the
    table of contents. If the return value is None, the given `section` will be
    used.

   :param app: the :class:`~sphinx.application.Sphinx` application object
   :param what: the type of the object which the docstring belongs to (one of
       ``"module"``, ``"class"``, ``"exception"``, ``"function"``, ``"method"``,
       ``"attribute"``)
   :param name: the fully qualified name of the object
   :param obj: the member object
   :param section: The section title that would be given to the object
       automatically (one of ``"Classes"``, ``"Exceptions"``, ``"Functions"``,
       ``"Methods"``, ``"Attributes"``, ``"Data"``)
   :param parent: The parent object holding the member `obj`


.. confval:: autodata_content

    As you can include the ``__init__`` method documentation for via the
    :confval:`autoclass_content <sphinx:autoclass_content>` configuration value,
    this configuration value lets you include the documentation from the
    ``__call__`` method. Possible values are

    class
        To only use the class documentation
    call
        To only use the documentation from the ``__call__`` method
    both
        To use the documentation from all.

    The default is ``'call'``


.. confval:: document_data

    To include the string representation of specific data objects. You may
    provide a list of fully qualified object names (e.g. in the form of
    ``'zipfile.ZipFile'``) or ``True`` or ``False``


.. confval:: not_document_data

    To exclude the string representation of specific data objects. You may
    provide a list of fully qualified object names (e.g. in the form of
    ``'zipfile.ZipFile'``) or ``True`` or ``False``
