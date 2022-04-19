"""Test module for autodocsumm.

**Disclaimer**

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
"""
import re
import bs4
import pytest
import sphinx


from autodocsumm import sphinx_version


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


def in_autosummary(what, html) -> bool:
    soup = bs4.BeautifulSoup(html)
    autosummaries = soup("table")
    found = False
    for tag in autosummaries:
        if tag.find_all("span", string=what):
            found = True
            break
    return found


class TestAutosummaryDocumenter:

    def test_module(self, app):
        app.build()
        html = get_html(app, 'test_module.html')
        assert in_autosummary("TestClass", html)
        assert in_autosummary("test_func", html)
        assert in_autosummary("test_method", html)
        assert in_autosummary("test_attr", html)

        # test whether the right objects are included
        assert in_autosummary("class_caller", html)
        assert 'Caller docstring for class attribute' in html

        # test whether the data is shown correctly
        assert in_autosummary("large_data", html)
        assert in_autosummary("small_data", html)

        try:
            assert 'Should be included' in html
        except AssertionError: # sphinx>=3.5
            assert (
                '<span class="pre">\'Should</span> '
                '<span class="pre">be</span> '
                '<span class="pre">included\'</span>'
            ) in html
            assert (
                '<span class="pre">\'Should</span> '
                '<span class="pre">be</span> '
                '<span class="pre">skipped\'</span>'
            ) not in html
        else:
            assert 'Should be skipped' not in html

        try:
            assert 'Should also be included' in html
        except AssertionError: # sphinx>=3.5
            assert (
                '<span class="pre">\'Should</span> '
                '<span class="pre">also</span> '
                '<span class="pre">be</span> '
                '<span class="pre">included\'</span>'
            ) in html
            assert (
                '<span class="pre">\'Should</span> '
                '<span class="pre">also</span> '
                '<span class="pre">be</span> '
                '<span class="pre">skipped\'</span>'
            ) not in html
        else:
            assert 'Should also be skipped' not in html

    def test_module_no_nesting(self, app):
        app.build()
        html = get_html(app, 'test_module_no_nesting.html')

        assert in_autosummary("TestClass", html)
        assert in_autosummary("test_func", html)

        # test whether the data is shown correctly
        assert in_autosummary("large_data", html)
        assert in_autosummary("small_data", html)

        # test that elements of TestClass are not autosummarized,
        # since nesting is disabled.
        assert not in_autosummary("test_method", html)
        assert not in_autosummary("test_attr", html)

        # test the members are still displayed
        assert re.search(
            r'<dt( class=".*")? id="dummy.Class_CallTest"( class=".*")*>',
            html,
        )

    def test_module_summary_only(self, app):
        app.build()
        html = get_html(app, 'test_module_summary_only.html')
        assert in_autosummary("TestClass", html)
        assert in_autosummary("test_func", html)

        # test whether the data is shown correctly
        assert in_autosummary("large_data", html)
        assert in_autosummary("small_data", html)

        assert not re.search(
            r'<dt( class=".*")? id="dummy.Class_CallTest"( class=".*")*>',
            html,
        )

    def test_module_with_title(self, app):
        app.build()
        html = get_html(app, 'test_module_title.html')
        assert in_autosummary("TestClass", html)
        assert in_autosummary("test_func", html)
        assert in_autosummary("test_method", html)
        assert in_autosummary("test_attr", html)

        # test whether the right objects are included
        assert in_autosummary("class_caller", html)
        assert 'Caller docstring for class attribute' in html

        # test whether the data is shown correctly
        assert in_autosummary("large_data", html)
        assert in_autosummary("small_data", html)
        try:
            assert 'Should be included' in  html
        except AssertionError: # sphinx>=3.5
            assert (
                '<span class="pre">\'Should</span> '
                '<span class="pre">be</span> '
                '<span class="pre">included\'</span>'
            ) in html
            assert (
                '<span class="pre">\'Should</span> '
                '<span class="pre">be</span> '
                '<span class="pre">skipped\'</span>'
            ) not in html
        else:
            assert 'Should be skipped' not in html
        try:
            assert 'Should also be included' in html
        except AssertionError: # sphinx>=3.5
            assert (
                '<span class="pre">\'Should</span> '
                '<span class="pre">also</span> '
                '<span class="pre">be</span> '
                '<span class="pre">included\'</span>'
            ) in html
            assert (
                '<span class="pre">\'Should</span> '
                '<span class="pre">also</span> '
                '<span class="pre">be</span> '
                '<span class="pre">skipped\'</span>'
            ) not in html
        else:
            assert 'Should also be skipped' not in html

    def test_module_nosignatures(self, app):
        app.build()

        html = get_html(app, 'test_module_nosignatures.html')
        assert in_autosummary("TestClass", html)
        assert in_autosummary("test_func", html)

        # test whether the data is shown correctly
        assert in_autosummary("large_data", html)
        assert in_autosummary("small_data", html)

        assert not re.search(
            r'<dt( class=".*")? id="dummy.Class_CallTest"( class=".*")*>',
            html,
        )
        assert '()' not in html

    def test_class(self, app):
        app.build()
        html = get_html(app, '/test_class.html')

        if sphinx_version[:2] > [3, 1]:
            assert in_autosummary("instance_attribute", html)
        elif sphinx_version[:2] < [3, 1]:
            assert in_autosummary("TestClass.instance_attribute", html)

        assert in_autosummary("test_method", html)
        assert in_autosummary("test_attr", html)

        # test escaping of *
        assert r'\*args' not in html
        assert r', \*\*kwargs' not in html
        assert '*args' in html
        assert '**kwargs' in html

        # test whether the right objects are included
        assert in_autosummary("class_caller", html)
        assert 'Caller docstring for class attribute' in html

        # test whether the data is shown correctly
        assert in_autosummary("large_data", html)
        assert in_autosummary("small_data", html)

        assert 'Should be skipped' not in html
        try:
            assert 'Should be included' in html
        except AssertionError: # sphinx>=3.5
            assert (
                '<span class="pre">\'Should</span> '
                '<span class="pre">be</span> '
                '<span class="pre">included\'</span>'
            ) in html

        assert 'DummySection' in html
        assert in_between(
            html, '<span class="pre">class_caller</span>', 'DummySection',
            'Attributes', 'Methods'
        ), 'class_caller Attribute not in the right Section!'

        # check if the InnerClass is in the Classes section (which ends with
        # the DummySection)
        assert in_between(
            html, '<span class="pre">InnerClass</span>', 'Classes',
            'DummySection'
        )

    @pytest.mark.skipif(
        sphinx_version[:2] < [3, 1], reason="Only available for sphinx>=3"
    )
    def test_class_order(self, app):
        app.build()
        html = get_html(app, '/test_class_order.html')

        if sphinx_version[:2] > [3, 1]:
            assert in_autosummary("instance_attribute", html)
        elif sphinx_version[:2] < [3, 1]:
            assert in_autosummary("TestClass.instance_attribute", html)

        assert in_autosummary("test_attr", html)
        assert in_autosummary("large_data", html)

        assert (
            html.index('<span class="pre">test_attr</span>')
            < html.index('<span class="pre">large_data</span>')
        )

    def test_class_summary_only(self, app):
        app.build()
        html = get_html(app, '/test_class_summary_only.html')

        if sphinx_version[:2] > [3, 1]:
            assert in_autosummary("instance_attribute", html)
        elif sphinx_version[:2] < [3, 1]:
            assert in_autosummary("TestClass.instance_attribute", html)

        assert in_autosummary("test_method", html)
        assert in_autosummary("test_attr", html)

        # test whether the right objects are included
        assert in_autosummary("class_caller", html)

        # test whether the data is shown correctly
        assert in_autosummary("large_data", html)
        assert in_autosummary("small_data", html)

        assert not re.search(
            r'<dt( class=".*")? id="dummy.TestClass.small_data"( class=".*")*>',
            html,
        )

    def test_class_nosignatures(self, app):
        app.build()
        html = get_html(app, '/test_class_nosignatures.html')

        if sphinx_version[:2] > [3, 1]:
            assert in_autosummary("instance_attribute", html)
        elif sphinx_version[:2] < [3, 1]:
            assert in_autosummary("TestClass.instance_attribute", html)

        assert in_autosummary("test_method", html)
        assert in_autosummary("test_attr", html)

        # test whether the right objects are included
        assert in_autosummary("class_caller", html)

        # test whether the data is shown correctly
        assert in_autosummary("large_data", html)
        assert in_autosummary("small_data", html)

        assert not re.search(
            r'<dt( class=".*")? id="dummy.TestClass.small_data"( class=".*")*>',
            html,
        )

        assert '()' not in html

    def test_inherited(self, app):
        app.build()
        html = get_html(app, '/test_inherited.html')
        assert in_autosummary("test_method", html)

    @pytest.mark.xfail
    def test_warnings_depreciation(self, app):
        with pytest.warns(
            sphinx.deprecation.RemovedInSphinx40Warning,
            r'(?s).*Autosummary.warnings',
        ):
            app.build()

    def test_autoclasssumm_inline(self, app):
        """Test an AutoDocSummDirective inline."""
        app.build()

        html = get_html(app, '/test_autoclasssumm_inline.html')

        methods_title = "<strong>Methods:</strong>"

        num_section_findings = len(re.findall(methods_title, html))

        assert num_section_findings == 1

        methods_start = html.index(methods_title)
        docstring_end = html.index("This is after the summary")

        assert docstring_end > methods_start

    def test_class_submodule(self, app):
        app.build()

        html = get_html(app, '/test_class_submodule.html')

        # check that hyperlink for instance method exists in summary table
        assert re.findall(r'<td>.*href="#dummy_submodule\.submodule1'
                          r'\.SubmoduleClass1\.func1".*</td>', html)

    def test_module_submodule(self, app):
        app.build()

        html = get_html(app, '/test_module_submodule.html')

        # check that hyperlink for class exists in summary table
        assert re.findall(r'<td>.*href="#dummy_submodule\.submodule2'
                          r'\.SubmoduleClass2".*</td>', html)

        # check that hyperlink for instance method exists in summary table
        assert re.findall(r'<td>.*href="#dummy_submodule\.submodule2'
                          r'\.SubmoduleClass2\.func2".*</td>', html)


class TestAutoDocSummDirective:
    """Test case for the :class:`autodocsumm.AutoDocSummDirective`."""

    def test_autoclasssumm(self, app):
        """Test building the autosummary of a class."""
        app.build()

        html = get_html(app, '/test_autoclasssumm.html')

        # the class docstring must not be in the html
        assert "Class test for autosummary" not in html

        # test if the methods and attributes are there in a table
        assert in_autosummary("test_method", html)
        assert in_autosummary("test_attr", html)

    def test_autoclasssumm_no_titles(self, app):
        """Test building the autosummary of a class."""
        app.build()

        html = get_html(app, '/test_autoclasssumm_no_titles.html')

        # the class docstring must not be in the html
        assert "Class test for autosummary" not in html

        # test if the methods and attributes are there in a table
        assert in_autosummary("test_method", html)
        assert in_autosummary("test_attr", html)

        assert "<strong>Methods</strong>" not in html

    def test_autoclasssumm_some_sections(self, app):
        """Test building the autosummary of a class with some sections only."""
        app.build()

        html = get_html(app, '/test_autoclasssumm_some_sections.html')

        # the class docstring must not be in the html
        assert "Class test for autosummary" not in html

        # test if the methods and attributes are there in a table
        assert not in_autosummary("test_method", html)
        assert in_autosummary("class_caller", html)
        assert in_autosummary("test_attr", html)

    def test_autoclasssumm_nosignatures(self, app):
        """Test building the autosummary of a class without signatures."""
        app.build()

        html = get_html(app, '/test_autoclasssumm_nosignatures.html')

        # the class docstring must not be in the html
        assert "Class test for autosummary" not in html

        # test if the methods and attributes are there in a table
        assert in_autosummary("test_method", html)
        assert in_autosummary("test_attr", html)

        assert '()' not in html

    def test_automodulesumm(self, app):
        """Test building the autosummary of a module."""
        app.build()

        html = get_html(app, '/test_automodulesumm.html')

        # the class docstring must not be in the html
        assert "Module for testing the autodocsumm" not in html

        # test if the classes, data and functions are there in a table
        assert in_autosummary("Class_CallTest", html)
        assert in_autosummary("large_data", html)
        assert in_autosummary("test_func", html)

    def test_automodulesumm_some_sections(self, app):
        """Test building the autosummary of a module with some sections only."""
        app.build()

        html = get_html(app, '/test_automodulesumm_some_sections.html')

        # the class docstring must not be in the html
        assert "Module for testing the autodocsumm" not in html

        # test if the classes, data and functions are there in a table
        assert not in_autosummary("Class_CallTest", html)
        assert in_autosummary("large_data", html)
        assert in_autosummary("test_func", html)

    def test_automodulesumm_nosignatures(self, app):
        """Test building the autosummary of a module without signatures."""
        app.build()

        html = get_html(app, '/test_automodulesumm_nosignatures.html')

        # the class docstring must not be in the html
        assert "Module for testing the autodocsumm" not in html

        # test if the classes, data and functions are there in a table
        assert in_autosummary("Class_CallTest", html)
        assert in_autosummary("large_data", html)
        assert in_autosummary("test_func", html)

        assert '()' not in html

    def test_empty(self, app):
        app.build()

        html = get_html(app, '/test_empty.html')

        assert not in_autosummary("product", html)
