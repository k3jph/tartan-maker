import pytest

from tartan_maker.colors import normalize_color
from tartan_maker.errors import ColorError


def test_normalize_named_colors():
    assert normalize_color("white") == "#FFFFFF"
    assert normalize_color("darkred") == "#8B0000"


def test_normalize_hex():
    assert normalize_color("#1959b9") == "#1959B9"
    assert normalize_color("1959B9") == "#1959B9"


def test_invalid_color():
    with pytest.raises(ColorError):
        normalize_color("not-a-real-color")
