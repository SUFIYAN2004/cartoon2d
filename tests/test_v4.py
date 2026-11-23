import shutil
import numpy as np
import pytest
from cartoon2d import *

def test_sprite():
    NewScene("plain")
    img = np.zeros((20, 10, 4), dtype=np.uint8); img[..., 0] = 255; img[..., 3] = 255
    s = DrawSprite(img, 50, 30, width=10); Move(s, (60, 30), 0, 3); Spin(s, 1, 0, 3)
    assert CurrentScene().frame(2).shape == (480, 800, 3)

def test_weather_and_flash():
    sc = NewScene("night")
    Snow(10, 0, 5); Rain(10, 0, 5); Flash(1, 4)
    assert sc.frame(3).shape[2] == 3
    assert sc.n_frames() == 6

def test_new_shapes():
    sc = NewScene("plain")
    for name in ("Windmill", "Snowman", "Lamp", "Ufo"):
        sc.add(SHAPES[name]("red", 50, 30))
    w = sc.shapes[0]; Spin3D(w, 1, 0, 3)
    assert sc.frame(2).shape == (480, 800, 3)

@pytest.mark.skipif(shutil.which("ffmpeg") is None, reason="no ffmpeg")
def test_mp4(tmp_path):
    NewScene(width_px=200)
    c = DrawBall("red", 10, 5); Move(c, (50, 5), 0, 3)
    p = tmp_path / "t.mp4"
    Save(str(p), show=False)
    assert p.stat().st_size > 0
