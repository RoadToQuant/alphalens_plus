import re
import alphalens_plus as ap


def test_version_is_string():
    assert isinstance(ap.__version__, str)


def test_version_format():
    assert re.match(r"^\d+\.\d+\.\d+", ap.__version__)
