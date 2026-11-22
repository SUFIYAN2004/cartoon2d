from cartoon2d import *

NewScene("day")
DrawMountain("slategray", 72, 18, 1.3)
DrawMountain("#7d8b99", 94, 18, 0.9)
sun = DrawSun("gold", 85, 50); Spin(sun, 0.25, 0, 80)
c1 = DrawCloud("white", 12, 47);       Move(c1, (62, 47), 0, 80, "linear")
c2 = DrawCloud("white", 60, 53, 0.7);  Move(c2, (108, 53), 0, 80, "linear")

DrawHouse("tomato", 14, 12)
DrawHouse("khaki", 34, 13, 0.85)
DrawTree("forestgreen", 52, 11)
DrawPine("darkgreen", 60, 12, 1.1)
for x in (24, 44, 68): DrawFlower("hotpink", x, 11)

DrawRect("#444444", 50, 0, w=100, h=9)                       # road
for x in range(6, 100, 16): DrawRect("white", x, 4, w=6, h=0.6)

car = DrawCar("royalblue", -12, 2.5)
Move(car, (112, 2.5), 0, 80, "linear"); Bounce(car, 0.35, 16, 0, 80)

bird = DrawBird("black", 5, 40, 0.8)
Move(bird, (95, 44), 0, 80, "linear"); Bob(bird, 1.5, 4, 0, 80)

walker = DrawPerson("purple", 20, 11, 0.55)
Move(walker, (46, 11), 0, 80, "linear"); Bounce(walker, 0.4, 12, 0, 80)

Say("Hello from cartoon2d!", 50, 33, 8, 60)
Save("town.gif")
