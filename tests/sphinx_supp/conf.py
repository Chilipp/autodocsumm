# -*- coding: utf-8 -*-

master_doc = 'index'

extensions = ['autodocsumm', 'sphinx.ext.napoleon']

autodoc_default_flags = ['show_inheritance', 'autosummary', 'members',
                         'undoc-members']

not_document_data = ['dummy.large_data', 'dummy.TestClass.small_data']
