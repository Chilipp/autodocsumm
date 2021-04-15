import sys
import re
import os.path as osp
import unittest
from sphinx_testing import with_app
import sphinx


from autodocsumm import sphinx_version


sphinx_supp = osp.abspath(osp.join(osp.dirname(__file__), 'sphinx_supp'))


sys.path.insert(0, sphinx_supp)


def in_between(full, sub, s0, *others):
    i0 = full.index(s0)
    try:
        last = min(filter(lambda i: i > i0, map(full.index, others)))
    except ValueError:  # empty sequence
        last = len(full)
    return full.index(sub) > i0 and full.index(sub) < last


def get_html(app, fname):
    with open(app.outdir + '/' + fname) as f:
        return f.read()


class TestAutosummaryDocumenter(unittest.TestCase):

    @with_app(buildername='html', srcdir=sphinx_supp,
              copy_srcdir_to_tmpdir=True)
    def test_module(self, app, status, warning):
        app.build()
        html = get_html(app, 'test_module.html')
        self.assertIn('<span class="pre">TestClass</span>', html)
        self.assertIn('<span class="pre">test_func</span>', html)
        self.assertIn('<span class="pre">test_method</span>', html)
        self.assertIn('<span class="pre">test_attr</span>', html)

        # test whether the right objects are included
        self.assertIn('<span class="pre">class_caller</span>', html)
        self.assertIn('Caller docstring for class attribute', html)

        # test whether the data is shown correctly
        self.assertIn('<span class="pre">large_data</span>', html)
        self.assertIn('<span class="pre">small_data</span>', html)

        try:
            self.assertIn('Should be included', html)
        except AssertionError: # sphinx>=3.5
            self.assertIn(
                '<span class="pre">\'Should</span> '
                '<span class="pre">be</span> '
                '<span class="pre">included\'</span>',
                html
            )
            self.assertNotIn(
                '<span class="pre">\'Should</span> '
                '<span class="pre">be</span> '
                '<span class="pre">skipped\'</span>',
                html
            )
        else:
            self.assertNotIn('Should be skipped', html)

        try:
            self.assertIn('Should also be included', html)
        except AssertionError: # sphinx>=3.5
            self.assertIn(
                '<span class="pre">\'Should</span> '
                '<span class="pre">also</span> '
                '<span class="pre">be</span> '
                '<span class="pre">included\'</span>',
                html
            )
            self.assertNotIn(
                '<span class="pre">\'Should</span> '
                '<span class="pre">also</span> '
                '<span class="pre">be</span> '
                '<span class="pre">skipped\'</span>',
                html
            )
        else:
            self.assertNotIn('Should also be skipped', html)

    @with_app(buildername='html', srcdir=sphinx_supp,
              copy_srcdir_to_tmpdir=True)
    def test_module_no_nesting(self, app, status, warning):
        app.build()
        html = get_html(app, 'test_module_no_nesting.html')

        self.assertIn('<span class="pre">TestClass</span>', html)
        self.assertIn('<span class="pre">test_func</span>', html)

        # test whether the data is shown correctly
        self.assertIn('<span class="pre">large_data</span>', html)
        self.assertIn('<span class="pre">small_data</span>', html)

        # test that elements of TestClass are not autosummarized, since nesting is disabled.
        try:
            self.assertNotIn('<span class="pre">test_method</span>', html)
            self.assertNotIn('<span class="pre">test_attr</span>', html)
        except AssertionError:  # sphinx>=3.5
            self.assertEqual(
                len(re.findall('<span class="pre">test_method</span>', html)),
                1,
            )
            self.assertEqual(
                len(re.findall('<span class="pre">test_attr</span>', html)),
                1,
            )

        # test the members are still displayed
        self.assertIn('<dt id="dummy.Class_CallTest">', html)

    @with_app(buildername='html', srcdir=sphinx_supp,
              copy_srcdir_to_tmpdir=True)
    def test_module_summary_only(self, app, status, warning):
        app.build()
        html = get_html(app, 'test_module_summary_only.html')
        self.assertIn('<span class="pre">TestClass</span>', html)
        self.assertIn('<span class="pre">test_func</span>', html)

        # test whether the data is shown correctly
        self.assertIn('<span class="pre">large_data</span>', html)
        self.assertIn('<span class="pre">small_data</span>', html)

        self.assertNotIn('<dt id="dummy.Class_CallTest">', html)

    @with_app(buildername='html', srcdir=sphinx_supp,
              copy_srcdir_to_tmpdir=True)
    def test_module_with_title(self, app, status, warning):
        app.build()
        html = get_html(app, 'test_module_title.html')
        self.assertIn('<span class="pre">TestClass</span>', html)
        self.assertIn('<span class="pre">test_func</span>', html)
        self.assertIn('<span class="pre">test_method</span>', html)
        self.assertIn('<span class="pre">test_attr</span>', html)

        # test whether the right objects are included
        self.assertIn('<span class="pre">class_caller</span>', html)
        self.assertIn('Caller docstring for class attribute', html)

        # test whether the data is shown correctly
        self.assertIn('<span class="pre">large_data</span>', html)
        self.assertIn('<span class="pre">small_data</span>', html)
        try:
            self.assertIn('Should be included', html)
        except AssertionError: # sphinx>=3.5
            self.assertIn(
                '<span class="pre">\'Should</span> '
                '<span class="pre">be</span> '
                '<span class="pre">included\'</span>',
                html
            )
            self.assertNotIn(
                '<span class="pre">\'Should</span> '
                '<span class="pre">be</span> '
                '<span class="pre">skipped\'</span>',
                html
            )
        else:
            self.assertNotIn('Should be skipped', html)
        try:
            self.assertIn('Should also be included', html)
        except AssertionError: # sphinx>=3.5
            self.assertIn(
                '<span class="pre">\'Should</span> '
                '<span class="pre">also</span> '
                '<span class="pre">be</span> '
                '<span class="pre">included\'</span>',
                html
            )
            self.assertNotIn(
                '<span class="pre">\'Should</span> '
                '<span class="pre">also</span> '
                '<span class="pre">be</span> '
                '<span class="pre">skipped\'</span>',
                html
            )
        else:
            self.assertNotIn('Should also be skipped', html)

    @with_app(buildername='html', srcdir=sphinx_supp,
        copy_srcdir_to_tmpdir=True)
    def test_module_nosignatures(self, app, status, warning):
        app.build()

        html = get_html(app, 'test_module_nosignatures.html')
        self.assertIn('<span class="pre">TestClass</span>', html)
        self.assertIn('<span class="pre">test_func</span>', html)

        # test whether the data is shown correctly
        self.assertIn('<span class="pre">large_data</span>', html)
        self.assertIn('<span class="pre">small_data</span>', html)

        self.assertNotIn('<dt id="dummy.Class_CallTest">', html)
        self.assertNotIn('()', html)

    @with_app(buildername='html', srcdir=sphinx_supp,
              copy_srcdir_to_tmpdir=True)
    def test_class(self, app, status, warning):
        app.build()
        html = get_html(app, '/test_class.html')

        if sphinx_version[:2] > [3, 1]:
            self.assertIn(
                '<span class="pre">instance_attribute</span>',
                html)
        elif sphinx_version[:2] < [3, 1]:
            self.assertIn(
                '<span class="pre">dummy.TestClass.instance_attribute</span>',
                html)

        self.assertIn('<span class="pre">test_method</span>', html)
        self.assertIn('<span class="pre">test_attr</span>', html)

        # test escaping of *
        self.assertNotIn(r'\*args', html)
        self.assertNotIn(r', \*\*kwargs', html)
        self.assertIn('*args', html)
        self.assertIn('**kwargs', html)

        # test whether the right objects are included
        self.assertIn('<span class="pre">class_caller</span>', html)
        self.assertIn('Caller docstring for class attribute', html)

        # test whether the data is shown correctly
        self.assertIn('<span class="pre">large_data</span>', html)
        self.assertIn('<span class="pre">small_data</span>', html)

        self.assertNotIn('Should be skipped', html)
        try:
            self.assertIn('Should be included', html)
        except AssertionError: # sphinx>=3.5
            self.assertIn(
                '<span class="pre">\'Should</span> '
                '<span class="pre">be</span> '
                '<span class="pre">included\'</span>',
                html
            )

        self.assertIn('DummySection', html)
        self.assertTrue(in_between(
            html, '<span class="pre">class_caller</span>', 'DummySection',
            'Attributes', 'Methods'),
            msg='class_caller Attribute not in the right Section!')

        # check if the InnerClass is in the Classes section (which ends with
        # the DummySection)
        self.assertTrue(in_between(
            html, '<span class="pre">InnerClass</span>', 'Classes',
            'DummySection'))

    @with_app(buildername='html', srcdir=sphinx_supp,
              copy_srcdir_to_tmpdir=True)
    @unittest.skipIf(
        sphinx_version[:2] < [3, 1], "Only available for sphinx>=3"
    )
    def test_class_order(self, app, status, warning):
        app.build()
        html = get_html(app, '/test_class_order.html')

        if sphinx_version[:2] > [3, 1]:
            self.assertIn(
                '<span class="pre">instance_attribute</span>',
                html)
        elif sphinx_version[:2] < [3, 1]:
            self.assertIn(
                '<span class="pre">dummy.TestClass.instance_attribute</span>',
                html)

        self.assertIn('<span class="pre">test_attr</span>', html)
        self.assertIn('<span class="pre">large_data</span>', html)

        self.assertLess(html.index('<span class="pre">test_attr</span>'),
                        html.index('<span class="pre">large_data</span>'))

    @with_app(buildername='html', srcdir=sphinx_supp,
              copy_srcdir_to_tmpdir=True)
    def test_class_summary_only(self, app, status, warning):
        app.build()
        html = get_html(app, '/test_class_summary_only.html')

        if sphinx_version[:2] > [3, 1]:
            self.assertIn(
                '<span class="pre">instance_attribute</span>',
                html)
        elif sphinx_version[:2] < [3, 1]:
            self.assertIn(
                '<span class="pre">dummy.TestClass.instance_attribute</span>',
                html)

        self.assertIn('<span class="pre">test_method</span>', html)
        self.assertIn('<span class="pre">test_attr</span>', html)

        # test whether the right objects are included
        self.assertIn('<span class="pre">class_caller</span>', html)

        # test whether the data is shown correctly
        self.assertIn('<span class="pre">large_data</span>', html)
        self.assertIn('<span class="pre">small_data</span>', html)

        self.assertNotIn('<dt id="dummy.TestClass.small_data">', html)

    @with_app(buildername='html', srcdir=sphinx_supp,
        copy_srcdir_to_tmpdir=True)
    def test_class_nosignatures(self, app, status, warning):
        app.build()
        html = get_html(app, '/test_class_nosignatures.html')

        if sphinx_version[:2] > [3, 1]:
            self.assertIn(
                '<span class="pre">instance_attribute</span>',
                html)
        elif sphinx_version[:2] < [3, 1]:
            self.assertIn(
                '<span class="pre">dummy.TestClass.instance_attribute</span>',
                html)

        self.assertIn('<span class="pre">test_method</span>', html)
        self.assertIn('<span class="pre">test_attr</span>', html)

        # test whether the right objects are included
        self.assertIn('<span class="pre">class_caller</span>', html)

        # test whether the data is shown correctly
        self.assertIn('<span class="pre">large_data</span>', html)
        self.assertIn('<span class="pre">small_data</span>', html)

        self.assertNotIn('<dt id="dummy.TestClass.small_data">', html)
        self.assertNotIn('()', html)

    @with_app(buildername='html', srcdir=sphinx_supp,
              copy_srcdir_to_tmpdir=True)
    def test_inherited(self, app, status, warning):
        app.build()
        html = get_html(app, '/test_inherited.html')
        self.assertIn('<span class="pre">test_method</span>', html)

    @with_app(buildername='html', srcdir=sphinx_supp,
              copy_srcdir_to_tmpdir=True)
    @unittest.skipIf(list(sys.version_info)[:2] <= [2, 7],
                     "not implemented for python 2.7")
    @unittest.skipIf(sphinx_version < [2, 0],
                     "not a problem for sphinx 2.7")
    @unittest.expectedFailure
    def test_warnings_depreciation(self, app, status, warning):
        with self.assertWarnsRegex(sphinx.deprecation.RemovedInSphinx40Warning,
                                   r'(?s).*Autosummary.warnings'):
            app.build()

    @with_app(buildername='html', srcdir=sphinx_supp,
              copy_srcdir_to_tmpdir=True)
    def test_autoclasssumm_inline(self, app, status, warning):
        """Test an AutoDocSummDirective inline."""
        app.build()

        html = get_html(app, '/test_autoclasssumm_inline.html')

        methods_title = "<strong>Methods:</strong>"

        num_section_findings = len(re.findall(methods_title, html))

        self.assertEqual(num_section_findings, 1)

        methods_start = html.index(methods_title)
        docstring_end = html.index("This is after the summary")

        self.assertGreater(docstring_end, methods_start)


class TestAutoDocSummDirective(unittest.TestCase):
    """Test case for the :class:`autodocsumm.AutoDocSummDirective`."""

    @with_app(buildername='html', srcdir=sphinx_supp,
              copy_srcdir_to_tmpdir=True)
    def test_autoclasssumm(self, app, status, warning):
        """Test building the autosummary of a class."""
        app.build()

        html = get_html(app, '/test_autoclasssumm.html')

        # the class docstring must not be in the html
        self.assertNotIn("Class test for autosummary", html)

        # test if the methods and attributes are there in a table
        self.assertIn('<span class="pre">test_method</span>', html)
        self.assertIn('<span class="pre">test_attr</span>', html)

    @with_app(buildername='html', srcdir=sphinx_supp,
              copy_srcdir_to_tmpdir=True)
    def test_autoclasssumm_no_titles(self, app, status, warning):
        """Test building the autosummary of a class."""
        app.build()

        html = get_html(app, '/test_autoclasssumm_no_titles.html')

        # the class docstring must not be in the html
        self.assertNotIn("Class test for autosummary", html)

        # test if the methods and attributes are there in a table
        self.assertIn('<span class="pre">test_method</span>', html)
        self.assertIn('<span class="pre">test_attr</span>', html)

        self.assertNotIn("<strong>Methods</strong>", html)

    @with_app(buildername='html', srcdir=sphinx_supp,
              copy_srcdir_to_tmpdir=True)
    def test_autoclasssumm_some_sections(self, app, status, warning):
        """Test building the autosummary of a class with some sections only."""
        app.build()

        html = get_html(app, '/test_autoclasssumm_some_sections.html')

        # the class docstring must not be in the html
        self.assertNotIn("Class test for autosummary", html)

        # test if the methods and attributes are there in a table
        self.assertNotIn('<span class="pre">test_method</span>', html)
        self.assertIn('<span class="pre">class_caller</span>', html)
        self.assertIn('<span class="pre">test_attr</span>', html)

    @with_app(buildername='html', srcdir=sphinx_supp,
        copy_srcdir_to_tmpdir=True)
    def test_autoclasssumm_nosignatures(self, app, status, warning):
        """Test building the autosummary of a class without signatures."""
        app.build()

        html = get_html(app, '/test_autoclasssumm_nosignatures.html')

        # the class docstring must not be in the html
        self.assertNotIn("Class test for autosummary", html)

        # test if the methods and attributes are there in a table
        self.assertIn('<span class="pre">test_method</span>', html)
        self.assertIn('<span class="pre">test_attr</span>', html)

        self.assertNotIn('()', html)

    @with_app(buildername='html', srcdir=sphinx_supp,
              copy_srcdir_to_tmpdir=True)
    def test_automodulesumm(self, app, status, warning):
        """Test building the autosummary of a module."""
        app.build()

        html = get_html(app, '/test_automodulesumm.html')

        # the class docstring must not be in the html
        self.assertNotIn("Module for testing the autodocsumm", html)

        # test if the classes, data and functions are there in a table
        self.assertIn('<span class="pre">Class_CallTest</span>', html)
        self.assertIn('<span class="pre">large_data</span>', html)
        self.assertIn('<span class="pre">test_func</span>', html)

    @with_app(buildername='html', srcdir=sphinx_supp,
              copy_srcdir_to_tmpdir=True)
    def test_automodulesumm_some_sections(self, app, status, warning):
        """Test building the autosummary of a module with some sections only."""
        app.build()

        html = get_html(app, '/test_automodulesumm_some_sections.html')

        # the class docstring must not be in the html
        self.assertNotIn("Module for testing the autodocsumm", html)

        # test if the classes, data and functions are there in a table
        self.assertNotIn('<span class="pre">Class_CallTest</span>', html)
        self.assertIn('<span class="pre">large_data</span>', html)
        self.assertIn('<span class="pre">test_func</span>', html)

    @with_app(buildername='html', srcdir=sphinx_supp,
        copy_srcdir_to_tmpdir=True)
    def test_automodulesumm_nosignatures(self, app, status, warning):
        """Test building the autosummary of a module without signatures."""
        app.build()

        html = get_html(app, '/test_automodulesumm_nosignatures.html')

        # the class docstring must not be in the html
        self.assertNotIn("Module for testing the autodocsumm", html)

        # test if the classes, data and functions are there in a table
        self.assertIn('<span class="pre">Class_CallTest</span>', html)
        self.assertIn('<span class="pre">large_data</span>', html)
        self.assertIn('<span class="pre">test_func</span>', html)

        self.assertNotIn('()', html)

    @with_app(buildername='html', srcdir=sphinx_supp,
              copy_srcdir_to_tmpdir=True)
    def test_empty(self, app, status, warning):
        app.build()

        html = get_html(app, '/test_empty.html')

        self.assertNotIn('<span class="pre">product</span>', html)


if __name__ == '__main__':
    unittest.main()
