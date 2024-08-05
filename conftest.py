import os.path as osp
import pytest
import sphinx
import sys
from packaging.version import Version

if Version(sphinx.__version__) < Version("8.0.0"):
    from sphinx.testing.path import path
else:
    from pathlib import Path as path

pytest_plugins = 'sphinx.testing.fixtures'


sphinx_supp = osp.abspath(osp.join(osp.dirname(__file__), "tests"))


@pytest.fixture(scope='session')
def rootdir():
    return path(sphinx_supp)


sys.path.insert(0, osp.join(sphinx_supp, "test-root"))
