"""
Some module
-----------

Just a dummy module with some class definition
"""


class MyClass(object):
    """Some class

    With some description"""

    def do_something(self):
        """Do something"""
        pass

    #: Any instance attribute
    some_attr = None

    #: Any other instance attribute
    some_other_attr = None


class MyException(object):
    """Some Exception

    With some description"""

    def do_something_exceptional(self):
        """Do something exceptional"""
        pass

    #: Any instance attribute
    some_exception_attr = None


#: Some module data
large_data = 'Whatever'
