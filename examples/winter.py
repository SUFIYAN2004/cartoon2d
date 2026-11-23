from cartoon2d import *

NewScene("night", width_px=640, ground="#dfe8f0")
DrawMoon("lightyellow", 15, 48)
DrawHouse("#8d6e63", 72, 12)
DrawPine("#0b3d2e", 90, 11, 1.2); DrawPine("#0b3d2e", 58, 11, 1.0)
DrawSnowman("white", 36, 10)
DrawLamp("gold", 50, 10)
mill = DrawWindmill("#cfd8dc", 10, 10); Spin3D(mill, 4, 0, 90)
ufo = DrawUfo("#9e9e9e", -10, 46)
Path(ufo, [(-10, 46), (30, 52), (60, 41), (110, 49)], 0, 90, "ease"); Bob(ufo, 1.2, 6, 0, 90)
Snow(80, 0, 90)
Say("Winter night", 50, 55, 5, 60, color="white")
Save("winter.gif", fps=20)
