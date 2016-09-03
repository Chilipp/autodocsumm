# -*- coding: utf-8 -*-
import inspect

master_doc = 'index'

extensions = ['autodocsumm']

autodoc_default_flags = ['show_inheritance', 'autosummary', 'members']

not_document_data = ['dummy.large_data', 'dummy.TestClass.small_data']

autodata_content = 'both'


def member_filter(app, what, name, obj, skip, options):
    import dummy
    if obj is dummy.TestClass.class_caller:
        return False
    return None


def group_member(app, what, name, obj, section, options):
    if name == 'class_caller':
        return 'DummySection'


def setup(app):
    app.connect('autodoc-skip-member', member_filter)
    app.connect('autodocsumm-grouper', group_member)
    app.setup_extension('sphinx.ext.napoleon')
