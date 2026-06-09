from tartan_maker import load_spec, render_svg, to_srt_block, to_srt_threadcount, visual_repeat, visual_stripes
from tartan_maker.model import Stripe


def write_tmp(tmp_path, text):
    path = tmp_path / "tartan.yaml"
    path.write_text(text, encoding="utf-8")
    return path


ASYM = """
name: Basu-Howard Tartan
sett_type: asymmetrical
colors:
  W: {name: White, color: white}
  LB: {name: Light Blue, color: "#1959B9"}
  MB: {name: Medium Blue, color: "#154C9E"}
  DB: {name: Dark Blue, color: "#103A79"}
  Y: {name: Gold, color: "#FEE46E"}
  DY: {name: Dark Gold, color: "#AC8800"}
sett: "W8 LB20 MB28 DB36 DY4 Y8 DY4 DB36 DY4 Y8 DY4 DB36 MB28 LB20"
"""

SYM = """
name: Example Symmetrical Tartan
sett_type: symmetrical
colors:
  B: {name: Blue, color: blue}
  W: {name: White, color: white}
  R: {name: Red, color: red}
  K: {name: Black, color: black}
  G: {name: Green, color: green}
sett: "B/24 W4 B24 R2 K24 G24 W/2"
"""


def test_asym_srt_rotation(tmp_path):
    spec = load_spec(write_tmp(tmp_path, ASYM))
    assert visual_repeat(spec) == 244
    assert to_srt_threadcount(spec).startswith("...W8")
    assert to_srt_threadcount(spec, rotate_asymmetrical=True).startswith("...DB36")
    block = to_srt_block(spec, rotate_asymmetrical=True)
    assert "Pallet:" in block
    assert "Threadcount:" in block
    assert "DB=#103A79#DARK BLUE" in block


def test_sym_visual_expansion_and_srt(tmp_path):
    spec = load_spec(write_tmp(tmp_path, SYM))
    assert visual_stripes(spec) == [
        Stripe("B", 24, True),
        Stripe("W", 4),
        Stripe("B", 24),
        Stripe("R", 2),
        Stripe("K", 24),
        Stripe("G", 24),
        Stripe("W", 2, True),
        Stripe("G", 24),
        Stripe("K", 24),
        Stripe("R", 2),
        Stripe("B", 24),
        Stripe("W", 4),
    ]
    assert to_srt_threadcount(spec) == "B/24 W4 B24 R2 K24 G24 W/2"


def test_svg_contains_expected_bits(tmp_path):
    spec = load_spec(write_tmp(tmp_path, ASYM))
    svg = render_svg(spec)
    assert "<svg" in svg
    assert 'viewBox="0 0 792 792"' in svg
    assert 'width="244" height="244"' in svg
    assert '<rect class="W" y="0" height="8"' in svg
    assert '<rect class="LB" y="8" height="20"' in svg
