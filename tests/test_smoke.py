from cartoon2d import *

def test_render_and_animate():
    NewScene("night")
    c = DrawCar("red", 10, 5)
    Move(c, (90, 5), 0, 5); Bounce(c, 1, 2, 0, 5); Spin(c, 1, 0, 5)
    assert CurrentScene().frame(3).shape == (480, 800, 3)

def test_all_shapes():
    sc = NewScene("plain")
    for cls in SHAPES.values(): sc.add(cls("red", 50, 30))
    assert sc.frame(0).shape[2] == 3

def test_chaining():
    NewScene()
    c = DrawBall("red", 0, 0)
    Move(c, (10, 0), 0, 10); Move(c, (10, 20), 10, 20)
    sc = CurrentScene(); sc._apply(20)
    assert (round(c.x), round(c.y)) == (10, 20)
