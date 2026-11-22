import random
from cartoon2d import *

NewScene("night")
r = random.Random(3)
for _ in range(25):
    s = DrawStar("white", r.uniform(2, 98), r.uniform(24, 58), r.uniform(.2, .5))
    Wiggle(s, 20, r.randint(1, 3), 0, 60)                    # twinkle
DrawMoon("lightyellow", 15, 48)
DrawHouse("#8d6e63", 75, 10)
DrawPine("#0b3d2e", 90, 9, 1.2)
rocket = DrawRocket("silver", 30, 8)
Move(rocket, (30, 75), 20, 60, "in"); Wiggle(rocket, 3, 10, 20, 60)
Save("night.gif")
