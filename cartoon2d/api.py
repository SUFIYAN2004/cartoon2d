import math, bisect
from .scene import Scene
from .shapes import *

SHAPES = {"Car": Car, "Sun": Sun, "Moon": Moon, "Star": Star, "House": House, "Tree": Tree,
          "Pine": Pine, "Cloud": Cloud, "Mountain": Mountain, "Flower": Flower, "Fence": Fence,
          "Person": Person, "Bird": Bird, "Boat": Boat, "Balloon": Balloon, "Rocket": Rocket,
          "Fish": Fish, "Ball": Ball, "Rect": Rect, "Circle": Disc, "Triangle": Triangle}

__all__ = ["SHAPES", "NewScene", "CurrentScene", "DrawText", "Move", "Path", "Orbit", "Rotate", "Spin",
           "Scale", "Fade", "Bounce", "Bob", "Wiggle", "Say", "Show", "Save", "Filmstrip", "Frames", "Gallery"]

_scene = None
def NewScene(theme="day", **kw):
    global _scene
    _scene = Scene(theme, **kw); return _scene
def CurrentScene():
    global _scene
    if _scene is None: _scene = Scene()
    return _scene
_s = CurrentScene

def _make(name, cls):
    def f(color, x, y, size=1, **kw):
        return _s().add(cls(color, x, y, size, **kw))
    f.__name__ = f.__qualname__ = "Draw" + name
    f.__doc__ = "Draw%s(color, x, y, size=1, alpha=1, rot=0, flip=False, z=0)" % name
    return f
for _n, _c in SHAPES.items():
    globals()["Draw" + _n] = _make(_n, _c)
    __all__.append("Draw" + _n)

def DrawText(text, color, x, y, size=1, **kw):
    return _s().add(Label(color, x, y, size, text=text, **kw))

# ---------- animation verbs: all take (shape, ..., start, end, ease) ----------
def _scalar(shape, prop, to, start, end, ease):
    a = shape._plan[prop]
    _s().track(shape, prop, lambda u: a + (to - a) * u, start, end, ease)
    shape._plan[prop] = to

def Move(shape, to, start=0, end=40, ease="ease"):
    x0, y0 = shape._plan["x"], shape._plan["y"]; x1, y1 = to
    _s().track(shape, "xy", lambda u: (x0 + (x1 - x0) * u, y0 + (y1 - y0) * u), start, end, ease)
    shape._plan["x"], shape._plan["y"] = x1, y1

def Rotate(shape, to, start=0, end=40, ease="ease"):   _scalar(shape, "rot", to, start, end, ease)
def Spin(shape, turns=1, start=0, end=40, ease="linear"):
    _scalar(shape, "rot", shape._plan["rot"] + 360 * turns, start, end, ease)
def Scale(shape, to, start=0, end=40, ease="ease"):    _scalar(shape, "size", to, start, end, ease)
def Fade(shape, to, start=0, end=20, ease="linear"):   _scalar(shape, "alpha", to, start, end, ease)

def Bounce(shape, height=6, times=3, start=0, end=40):
    _s().track(shape, "y", lambda u: height * abs(math.sin(math.pi * times * u)), start, end, "linear", "add")
def Bob(shape, height=2, times=3, start=0, end=40):
    _s().track(shape, "y", lambda u: height * math.sin(2 * math.pi * times * u), start, end, "linear", "add")
def Wiggle(shape, degrees=10, times=3, start=0, end=40):
    _s().track(shape, "rot", lambda u: degrees * math.sin(2 * math.pi * times * u), start, end, "linear", "add")

def Orbit(shape, center, radius, start=0, end=60, turns=1, angle=0, ease="linear"):
    cx, cy = center; a0 = math.radians(angle)
    pos = lambda u: (cx + radius * math.cos(a0 + 2 * math.pi * turns * u),
                     cy + radius * math.sin(a0 + 2 * math.pi * turns * u))
    _s().track(shape, "xy", pos, start, end, ease)
    shape._plan["x"], shape._plan["y"] = pos(1.0)

def Path(shape, points, start=0, end=40, ease="linear", by="length"):
    """Follow a list of (x, y). by='length' = constant speed, by='index' = one point per equal time step."""
    pts = [tuple(p) for p in points]
    if len(pts) < 2: raise ValueError("Path needs at least 2 points")
    cum = [0.0]
    for a, b in zip(pts, pts[1:]): cum.append(cum[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    def fn(u):
        if by == "index":
            f = u * (len(pts) - 1); i = min(int(f), len(pts) - 2); r = f - i
        else:
            d = u * cum[-1]; i = min(bisect.bisect_right(cum, d) - 1, len(pts) - 2)
            seg = cum[i + 1] - cum[i]; r = 0.0 if seg == 0 else (d - cum[i]) / seg
        return (pts[i][0] + (pts[i + 1][0] - pts[i][0]) * r, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * r)
    _s().track(shape, "xy", fn, start, end, ease)
    shape._plan["x"], shape._plan["y"] = pts[-1]

def Say(text, x, y, start=0, end=40, color="black", size=1):
    t = DrawText(text, color, x, y, size, alpha=0)
    Fade(t, 1, start, start + 3)
    if end - start > 6: Fade(t, 0, end - 3, end)
    return t

# ---------- output ----------
def Show(t=0):                              _s().show(t)
def Save(path="scene.gif", fps=20, hold=0): return _s().save(path, fps, hold)
def Filmstrip(n=6):                         return _s().filmstrip(n)
def Frames():                               return _s().frames()

def Gallery():
    """Draw every shape with its name, to check the install."""
    sc = NewScene("plain", ground_h=0)
    colors = ["tomato", "royalblue", "gold", "seagreen", "orchid", "darkorange", "teal"]
    for i, (name, cls) in enumerate(SHAPES.items()):
        col, row = i % 8, i // 8
        x, base = 6.5 + col * 12.4, 44 - row * 19
        sc.add(cls(colors[i % len(colors)], x, base + (5 if cls.origin == "center" else 0), 0.55))
        sc.add(Label("black", x, base - 3.5, 0.5, text=name))
    sc.show()
    return sc
# ---------------- v0.3: depth, camera, walk, drive, 3D ----------------
for _n in ("Cube", "Sphere"):
    SHAPES[_n] = globals()[_n]
    globals()["Draw" + _n] = _make(_n, SHAPES[_n])
    __all__.append("Draw" + _n)

def Say(text, x, y, start=0, end=40, color="black", size=1):
    t = DrawText(text, color, x, y, size, alpha=0)
    t.hud = True                                  # captions stay on screen when the camera moves
    Fade(t, 1, start, start + 3)
    if end - start > 6: Fade(t, 0, end - 3, end)
    return t

def Depth(shape, to, start=0, end=40, ease="ease"): _scalar(shape, "depth", to, start, end, ease)

def _phase(shape, to, start, end, ease):
    _s().track(shape, "phase", lambda u, a=shape._plan["phase"]: a + (to - a) * u, start, end, ease)
    shape._plan["phase"] = to

def Walk(shape, steps=4, start=0, end=40):
    """Swing arms and legs; `steps` = full leg cycles. Use with Move."""
    _phase(shape, shape._plan["phase"] + 2 * math.pi * steps, start, end, "linear")

def Spin3D(shape, turns=1, start=0, end=40, ease="linear"):
    """Turn a Cube around its vertical axis."""
    _phase(shape, shape._plan["phase"] + 2 * math.pi * turns, start, end, ease)

def Drive(car, to, start=0, end=60, ease="linear"):
    """Move a car and spin its wheels by the distance travelled."""
    dx = to[0] - car._plan["x"]
    spin = -dx / (1.8 * car._plan["size"])
    Move(car, to, start, end, ease)
    _phase(car, car._plan["phase"] + spin, start, end, ease)

def CameraMove(to, start=0, end=40, ease="ease"):
    cam = _s().camera; x0, y0 = cam._plan["x"], cam._plan["y"]; x1, y1 = to
    _s().track(cam, "xy", lambda u: (x0 + (x1 - x0) * u, y0 + (y1 - y0) * u), start, end, ease)
    cam._plan["x"], cam._plan["y"] = x1, y1

def CameraZoom(to, start=0, end=40, ease="ease"): _scalar(_s().camera, "zoom", to, start, end, ease)

def Follow(shape, start=0, offset=(0, 0), axis="x"):
    """Camera tracks the shape from `start` to the end of the scene. axis='x' or 'xy'."""
    _s().follows.append(dict(shape=shape, start=start, offset=offset, axis=axis))

def Shake(amount=1.5, start=0, end=20):
    cam = _s().camera
    _s().track(cam, "x", lambda u: amount * math.sin(2 * math.pi * 13 * u) * (1 - u), start, end, "linear", "add")
    _s().track(cam, "y", lambda u: amount * math.sin(2 * math.pi * 17 * u) * (1 - u), start, end, "linear", "add")

__all__ += ["Depth", "Walk", "Spin3D", "Drive", "CameraMove", "CameraZoom", "Follow", "Shake"]
