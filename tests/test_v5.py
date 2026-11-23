import os, shutil, pytest
from cartoon2d import *

def test_talk_and_dialogue():
    sc = NewScene("day")
    m = Cast(Mia=("Person", "orchid", 0.7)).Mia(30, 11)
    end = Dialogue(lambda s: int(s * 10), [(m, "Hello there, this is a long line that should wrap")], start=0.2)
    assert end > 0.2
    assert sc.frame(5).shape == (480, 800, 3)

@pytest.mark.skipif(shutil.which("ffmpeg") is None, reason="no ffmpeg")
def test_episode(tmp_path):
    ep = Episode("T", fps=5, width_px=160)
    ep.card("Hi", seconds=1)
    @ep.scene("a", seconds=1)
    def a(T): DrawBall("red", 20, 20)
    out = ep.render(str(tmp_path / "t.mp4"), workdir=str(tmp_path / "w"))
    assert os.path.getsize(out) > 0
