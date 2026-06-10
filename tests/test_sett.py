import pytest

from tartan_maker.errors import SettParseError
from tartan_maker.model import Stripe
from tartan_maker.sett import detect_sett_type, parse_sett_string, stripes_to_sett_string
from tartan_maker.model import SettType


def test_parse_plain_sett():
    assert parse_sett_string("W8 LB20") == [Stripe("W", 8), Stripe("LB", 20)]


def test_parse_pivots():
    assert parse_sett_string("B/24 W4 W/2") == [
        Stripe("B", 24, True),
        Stripe("W", 4),
        Stripe("W", 2, True),
    ]


def test_parse_ellipsis():
    assert parse_sett_string("...B24 W4...") == [Stripe("B", 24), Stripe("W", 4)]


def test_detect_sett_type():
    assert detect_sett_type("...B24 W4...") == SettType.ASYMMETRICAL
    assert detect_sett_type("B/24 W4 W/2") == SettType.SYMMETRICAL


def test_format_sett():
    assert stripes_to_sett_string([Stripe("B", 24, True), Stripe("W", 4)]) == "B/24 W4"


@pytest.mark.parametrize("bad", ["", "b24", "B0", "B-24", "B/", "24B", "B 24"])
def test_bad_tokens(bad):
    with pytest.raises(SettParseError):
        parse_sett_string(bad)
