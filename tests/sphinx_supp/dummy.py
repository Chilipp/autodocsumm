# -*- coding: utf-8 -*-
"""
Module for testing the autodocsumm

Just a dummy module with some class definitions
"""


#: to test if the data is included
test_data = None


def test_func():
    """Test if function is contained in autosummary"""
    pass


class Class_CallTest(object):
    """A class defining a __call__ method"""

    def __get__(self, instance, owner):
        return self

    def __set__(self, instance, value):
        """Actually not required. We just implement it to ensure the python
        "help" function works well"""
        pass

    def __call__(self, a, b):
        """
        Caller docstring for class attribute

        Parameters
        ----------
        a: any
            dummy parameter
        b: anything else
            second dummy parameter"""
        pass


class TestClass(object):
    """Class test for autosummary"""

    def __init__(self):
        #: This is an instance attribute
        self.instance_attribute = 1

    def test_method(self):
        """Test if the method is included"""
        pass

    def test_method_args_kwargs(self, *args, **kwargs):
        """The stars at args and kwargs should not be escaped"""

    class InnerClass(object):
        """A test for an inner class"""

    #: to test if the class attribute is included
    test_attr = None

    class_caller = Class_CallTest()

    #: data to be included
    large_data = 'Should be included'

    #: data to be skipped
    small_data = 'Should be skipped'


class InheritedTestClass(TestClass):
    """Class test for inherited attributes"""


class TestClassWithInlineAutoClassSumm:
    """Class test for the autodocsummary inline

    .. autoclasssumm:: TestClassWithInlineAutoClassSumm

    This is after the summary.
    """

    def test_method_of_inline_test(self):
        """A test method."""
        pass


#: data to be skipped
large_data = 'Should also be skipped'

#: data to be included
small_data = 'Should also be included'
