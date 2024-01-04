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

See also the usage in the :ref:`examples` section.

The other additional flags lets you control what should be in the autosummary
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
(i.e. ``private-members`` or ``members``), but they only affect the
autosummary table (see the example in :ref:`summary-table-example`).

``autosummary-no-nesting``
    The new additional flag ``autosummary-no-nesting`` only generates
    autosummary tables for a module, but not for members within. See
    example about :ref:`no-nesting-example`.
``autosummary-sections``
    Select which sections to generate the autosummary for. Usage is like
    ``:autosummary-sections: Methods ;; Attributes``. When omitted, all sections
    are generated. See the example about :ref:`select-sections-example`
``autosummary-no-titles``
    Do not add section titles above each autosummary table
``autosummary-force-inline``
    Force adding the autosummary, even it is already contained in the class
    or module docstring. See the example about :ref:`autosummary-position-example`
``autosummary-nosignatures``
    Do not show function signatures in the summary table.


.. _directives:

Directives
----------

.. rst:directive:: autoclasssumm

    This class generates the autosummary tables for the given class. You can
    use the same options as for the ``autoclass`` directive. You can select a
    specific section and omit the title via::

        .. autoclasssumm:: MyClass
            :autosummary-sections: Methods
            :autosummary-no-titles:

    By default, this directives also sets the `:members:` option unless you
    specify `:no-members`.

.. rst:directive:: automodulesumm

    The same as the ``autoclasssumm`` directive, just for a module.


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


.. confval:: autodocsumm_section_sorter

   When ``True`` the summarizing sections will be sorted alphanumerically by
   their section title. Alternatively a callable can be set that is passed to
   :func:`sorted` as key argument to sort the the summary sections by their
   name.
   The default value is ``None``.
   Example usage with a tuple that defines an arbitrary order:

   .. code-block:: python

       sections_order = ("Public methods", "Attributes", "Private methods")
       autodocsumm_section_sorter = lambda title: sections_order.index(title)

   An example for cases that only ensures that "Constructors" are always listed
   first and "Attributes" while not failing when encountering undefined section
   weights:

   .. code-block:: python

       section_weights = {"Attributes": 100, "Constructors": -100}
       autodocsumm_section_sorter = lambda title: sections_weights.get(title, 0)
