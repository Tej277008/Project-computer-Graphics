# Tiny autograder for local sanity checks (students run after implementation)
from rasterizer import Rasterizer
import numpy as np

try:
    r = Rasterizer(64, 64, samples=1)
    r.draw_triangle([8,8],[56,10],[16,48],[1,0,0],[0,1,0],[0,0,1])
    img = r.resolve()
    assert img.shape == (64,64,3)
    assert img.sum() > 0
    print("P1 tiny autograder: PASS")
except NotImplementedError as e:
    print("P1 tiny autograder: NOT READY —", e)