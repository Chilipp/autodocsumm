.. confvals:

Configuration values and events
===============================

The module provides 3 additional configuration values and one event.
Furthermore it provides the *autosummary* flag for the usage in the
*automodule* and *autoclass* directive. See also the :ref:`examples` section
for their usage.


.. event:: autodocsumm-grouper (app, what, name, obj, section, options, parent)

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
