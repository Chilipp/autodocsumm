import os.path as osp
import sys
import pytest

from sphinx.testing.path import path

pytest_plugins = 'sphinx.testing.fixtures'



sphinx_supp = osp.abspath(osp.join(osp.dirname(__file__), "tests"))


@pytest.fixture(scope='session')
def rootdir():
    return path(sphinx_supp)


sys.path.insert(0, osp.join(sphinx_supp, "test-root"))
