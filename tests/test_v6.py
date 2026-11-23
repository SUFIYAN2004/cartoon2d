import pytest
from cartoon2d import *
from cartoon2d.shapes_more import CATALOG, Procedural

def test_catalogue_size_and_search():
    assert len(Shapes()) >= 1000
    assert "flower_8_long" in Find("flower") and "Car" in Find("car")

def test_every_shape_builds():
    for name, (kind, params) in CATALOG.items():
        assert len(Procedural(kind, params, "red", 50, 30).parts()) > 0, name

def test_one_per_family_renders():
    sc = NewScene("plain"); seen = set()
    for name, (kind, _) in CATALOG.items():
        if kind not in seen:
            seen.add(kind); DrawShape(name, "random", 10 + 5 * len(seen), 30)
    s = RandomShape(50, 30, seed=1); Spin(s, 1, 0, 3); Move(s, (60, 30), 0, 3)
    assert sc.frame(2).shape == (480, 800, 3) and len(seen) == 16

def test_svg():
    pytest.importorskip("svgpath2mpl")
    sc = NewScene("plain")
    DrawSVG('<svg viewBox="0 0 10 10"><path d="M0 0 L10 0 L5 10 Z" fill="#ff0000"/></svg>', 50, 20, width=10)
    assert sc.frame(0).shape == (480, 800, 3)
