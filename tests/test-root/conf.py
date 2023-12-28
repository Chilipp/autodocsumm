# -*- coding: utf-8 -*-
import sys
import sphinx
sys.path.insert(0, '.')

master_doc = 'index'

extensions = ['autodocsumm']

if tuple(map(int, sphinx.__version__.split('.')[:2])) < (2, 1):
    autodoc_default_flags = ['show_inheritance', 'autosummary', 'members']
else:
    autodoc_default_options = {
        'show_inheritance': True,
        'autosummary': True,
        'members': True
        }

not_document_data = [
    'dummy.large_data', 'dummy.TestClass.small_data',
    'dummy_title.large_data', 'dummy_title.TestClass.small_data']

autodoc_typehints = "description"

autodata_content = 'both'

autodocsumm_section_sorter = lambda a: a


def member_filter(app, what, name, obj, skip, options):
    import dummy
    import dummy_title
    if (obj is dummy.TestClass.class_caller or
            obj is dummy_title.TestClass.class_caller):
        return False
    return None


def group_member(app, what, name, obj, section, parent):
    if name == 'class_caller':
        return 'DummySection'


def setup(app):
    app.connect('autodoc-skip-member', member_filter)
    app.connect('autodocsumm-grouper', group_member)
    app.setup_extension('sphinx.ext.napoleon')
