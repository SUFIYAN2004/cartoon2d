from cartoon2d import *

NewScene("day", width_px=560)
for x in range(-80, 500, 60):  DrawMountain("#9fb2c4", x, 18, 3.2, depth=6)   # far, slow
for x in range(-40, 460, 40):  DrawMountain("slategray", x, 18, 1.6, depth=3)

sun = DrawSun("gold", 85, 50); sun.hud = True; Spin(sun, 0.5, 0, 150)
for x, y, v in [(10, 48, 1), (70, 54, .7)]:
    c = DrawCloud("white", x, y, v); c.hud = True; Move(c, (x + 40, y), 0, 150, "linear")

for i, x in enumerate(range(20, 460, 38)):
    if i % 3 == 0: DrawHouse(["tomato", "khaki", "lightskyblue"][i // 3 % 3], x, 14, .9, depth=1)
    elif i % 2:    DrawTree("forestgreen", x, 14, 1, depth=1.5)
    else:          DrawPine("darkgreen", x, 14, 1.1, depth=1.5)

for x in range(0, 460, 100): DrawRect("#444444", x, 0, w=101, h=9)
for x in range(0, 460, 16):  DrawRect("white", x, 4, w=6, h=.6)

car = DrawCar("royalblue", 10, 3, shadow=True)
Drive(car, (330, 3), 0, 150); Bounce(car, 0.3, 40, 0, 150)
Follow(car, offset=(20, 0))

walker = DrawPerson("purple", 70, 12, .6, depth=1, shadow=True)
Move(walker, (170, 12), 0, 150, "linear"); Walk(walker, 28, 0, 150)

cube = DrawCube("orange", 120, 11, 1.1, depth=1, shadow=True)
Spin3D(cube, 3, 0, 150)

Say("cartoon2d", 50, 52, 5, 60)
CameraZoom(1.25, 110, 150)
Save("road_trip.gif", fps=25)
