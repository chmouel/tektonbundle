import glob
import os.path

import pytest


@pytest.fixture(scope="session")
def testdata():
    ret = {}
    for fname in glob.glob(
            os.path.join(os.path.dirname(__file__), 'yamls/*.y*ml')):
        ret[os.path.splitext(os.path.basename(fname))[0]] = fname
    return ret
