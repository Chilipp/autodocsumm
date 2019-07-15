.. _examples:

Examples
========

.. toctree::
    :hidden:

    Demo Module <demo_module>
    Demo Class <demo_class>
    Demo Grouper <demo_grouper>

Including a table of contents
-----------------------------
Consider for example the following module in ``dummy.py``:

.. literalinclude:: dummy.py

The *autosummary* flag introduces a small table of contents. So::

    .. automodule:: dummy
        :members:
        :autosummary:

produces :ref:`this <demo_module>`. And::

    .. autoclass:: dummy.SomeClass
        :members:
        :autosummary:

produces :ref:`this <demo_class>`.

By default, module members are (mainly) grouped according into *Functions*,
*Classes* and *Data*, class members are grouped into *Methods* and
*Attributes*. But you can also provide alternative section names by connecting
to the :event:`autodocsumm-grouper` event. For example, if you include::

    def example_grouper(app, what, name, obj, section, options, parent):
        import dummy
        if parent is dummy.MyClass and name == 'some_other_attr':
            return 'Alternative Section'


    def setup(app):
        app.connect('autodocsumm-grouper', example_grouper)

in your *conf.py*, you get :ref:`this <demo_grouper>`.

Note that you can also include the *autosummary* flag in the
:confval:`autodoc_default_options` configuration value


Including the ``__call__`` method
---------------------------------
Suppose you have a descriptor with a ``__call__`` method (i.e. somewhat like
a method with additional features).

.. literalinclude:: call_demo.py

Then, if you set ``autodata_content = 'both'`` in your *conf.py* you get via::

    .. autoclass:: call_demo.MyClass
        :noindex:
        :members:
        :undoc-members:

.. autoclass:: call_demo.MyClass
    :noindex:
    :members:
    :undoc-members:


Skip large data representations
-------------------------------
You can exclude large data representations via the :confval:`not_document_data`
and :confval:`document_data` configuration values.

Suppose you have a dictionary with a very large representation, e.g. in the
file `no_data_demo.py`

.. literalinclude:: no_data_demo.py

which you convert to

.. autodata:: keep_data_demo.d
    :noindex:

You can skip this if you specify ``not_document_data = ['no_data_demo.d']`` in
your *conf.py*. Then you get

.. autodata:: no_data_demo.d
    :noindex:
