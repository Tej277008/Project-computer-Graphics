import numpy as np
import pytest
from rasterizer import Rasterizer


def test_rasterizer_shapes():
    r = Rasterizer(64, 48, samples=1)
    assert r.fb.shape == (48, 64, 3)


def test_draw_triangle_not_implemented():
    r = Rasterizer(32, 32, samples=1)
    with pytest.raises(NotImplementedError):
        r.draw_triangle([5,5],[20,6],[6,20],[1,0,0],[0,1,0],[0,0,1])


def test_resolve_not_implemented():
    r = Rasterizer(32, 32, samples=4)
    with pytest.raises(NotImplementedError):
        r.resolve()