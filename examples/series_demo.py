from cartoon2d import *

cast = Cast(Mia=("Person", "orchid", 0.7), Max=("Person", "teal", 0.7))
ep = Episode("Mia and Max - The Race", fps=15, width_px=480)
ep.card("Mia & Max\nEpisode 1: The Race", seconds=3)

@ep.scene("Park", seconds=18)
def park(T):
    DrawMountain("slategray", 75, 18, 1.2)
    DrawTree("forestgreen", 10, 13); DrawPine("darkgreen", 92, 13, 1.1)
    sun = DrawSun("gold", 85, 50); sun.hud = True; Spin(sun, 0.3, 0, T(18))
    cloud = DrawCloud("white", 15, 50); cloud.hud = True; Move(cloud, (70, 50), 0, T(18), "linear")
    mia = cast.Mia(30, 11); mx = cast.Max(45, 11)
    t = Dialogue(T, [(mia, "Max! Race you to the big tree!"), (mx, "You're on, Mia!")], start=1)
    Move(mia, (80, 11), T(t), T(t + 5)); Walk(mia, 10, T(t), T(t + 5))
    Move(mx, (88, 11), T(t), T(t + 6)); Walk(mx, 12, T(t), T(t + 6))
    Dialogue(T, [(mia, "I win!"), (mx, "Rematch!")], start=t + 6.3)

@ep.scene("Sunset", seconds=12, theme="sunset")
def sunset(T):
    DrawMountain("#5c4a7a", 30, 18, 1.4)
    DrawHouse("khaki", 82, 12)
    mia = cast.Mia(35, 11); mx = cast.Max(50, 11)
    ufo = DrawUfo("silver", -10, 50)
    Path(ufo, [(-10, 50), (45, 40), (62, 36)], T(0.5), T(4), "ease"); Bob(ufo, 1, 6, T(0.5), T(4))
    Dialogue(T, [(mia, "Max... is that a UFO?!"), (mx, "I think it wants a rematch!")], start=4.2)
    Shake(1.2, T(4), T(5))

ep.card("To be continued...", seconds=3)

if __name__ == "__main__":
    ep.estimate()
    ep.render()
