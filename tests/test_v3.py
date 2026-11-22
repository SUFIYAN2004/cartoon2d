from cartoon2d import *

def test_depth_identity_and_far_is_smaller():
    sc = NewScene(); s = DrawBall("red", 30, 10)
    got = sc._project(s)[:3]
    assert all(abs(a - b) < 1e-9 for a, b in zip(got, (30, 10, 1)))
    s.depth = 4
    assert sc._project(s)[2] < 1

def test_follow_and_drive():
    sc = NewScene(); car = DrawCar("red", 0, 3)
    Drive(car, (200, 3), 0, 10); Follow(car)
    sc._apply(10)
    assert abs(sc.camera.x - car.x) < 1e-9 and abs(car.x - 200) < 1e-9

def test_new_shapes_render():
    sc = NewScene("plain")
    c = DrawCube("orange", 30, 20, shadow=True); Spin3D(c, 1, 0, 5)
    p = DrawPerson("purple", 60, 20); Walk(p, 4, 0, 5)
    DrawSphere("teal", 80, 30)
    CameraZoom(1.3, 0, 5); Shake(1, 0, 5)
    assert sc.frame(3).shape == (480, 800, 3)
