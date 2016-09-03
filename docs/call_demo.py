"""
Some module
-----------

Just a dummy module with some class definition
"""


class CallableDescriptor(object):
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


class MyClass(object):
    """Some class

    With some description"""

    do_something = CallableDescriptor()
