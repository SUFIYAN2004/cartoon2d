import math, bisect, random, zlib
from .scene import Scene
from .shapes import *
from .shapes_more import Procedural, SvgShape, CATALOG

SHAPES = {"Car": Car, "Sun": Sun, "Moon": Moon, "Star": Star, "House": House, "Tree": Tree,
          "Pine": Pine, "Cloud": Cloud, "Mountain": Mountain, "Flower": Flower, "Fence": Fence,
          "Person": Person, "Bird": Bird, "Boat": Boat, "Balloon": Balloon, "Rocket": Rocket,
          "Fish": Fish, "Ball": Ball, "Rect": Rect, "Circle": Disc, "Triangle": Triangle,
          "Cube": Cube, "Sphere": Sphere, "Windmill": Windmill, "Snowman": Snowman,
          "Lamp": Lamp, "Ufo": Ufo}

__all__ = ["SHAPES", "NewScene", "CurrentScene", "DrawText", "Move", "Path", "Orbit", "Rotate", "Spin",
           "Scale", "Fade", "Bounce", "Bob", "Wiggle", "Say", "Show", "Save", "Filmstrip", "Frames", "Gallery",
           "Depth", "Walk", "Spin3D", "Drive", "CameraMove", "CameraZoom", "Follow", "Shake",
           "DrawSprite", "Snow", "Rain", "Flash", "Talk", "Dialogue", "Cast",
           "Shapes", "Find", "DrawShape", "RandomShape", "DrawSVG", "Sheet"]

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
    f.__doc__ = "Draw%s(color, x, y, size=1, alpha=1, rot=0, flip=False, z=0, depth=0, shadow=False)" % name
    return f
for _n, _c in SHAPES.items():
    globals()["Draw" + _n] = _make(_n, _c)
    __all__.append("Draw" + _n)

def DrawText(text, color, x, y, size=1, **kw):
    return _s().add(Label(color, x, y, size, text=text, **kw))

def DrawSprite(path, x, y, size=1, width=10, **kw):
    """Your own PNG (or RGBA array) as a shape: DrawSprite('cat.png', 50, 12, width=12)."""
    return _s().add(Sprite(path, x, y, size, width=width, **kw))

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
def Depth(shape, to, start=0, end=40, ease="ease"):    _scalar(shape, "depth", to, start, end, ease)

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
    t.hud = True                                  # captions stay on screen when the camera moves
    Fade(t, 1, start, start + 3)
    if end - start > 6: Fade(t, 0, end - 3, end)
    return t

def _phase(shape, to, start, end, ease):
    a = shape._plan["phase"]
    _s().track(shape, "phase", lambda u: a + (to - a) * u, start, end, ease)
    shape._plan["phase"] = to

def Walk(shape, steps=4, start=0, end=40):
    """Swing arms and legs; `steps` = full leg cycles. Use with Move."""
    _phase(shape, shape._plan["phase"] + 2 * math.pi * steps, start, end, "linear")

def Spin3D(shape, turns=1, start=0, end=40, ease="linear"):
    """Turn a Cube around its vertical axis, or turn Windmill blades."""
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

# ---------- weather ----------
def _particles(kind, n, start, end, seed, color, speed):
    r, sc = random.Random(seed), _s()
    top = sc.h + 5
    for _ in range(n):
        x0 = r.uniform(-5, sc.w + 5)
        if kind == "snow":
            p = Disc(color, x0, top, 1, r=r.uniform(.25, .6), z=5); drift = r.uniform(-4, 4)
        else:
            p = Rect(color, x0, top, 1, w=.15, h=r.uniform(1.2, 2.2), rot=8, z=5); drift = -3
        p.hud = True
        sc.add(p)
        period = r.uniform(*speed)
        t = start + r.uniform(0, period)
        while t < end:
            b = min(t + period, end); f = (b - t) / period
            sc.track(p, "xy", lambda u, x0=x0, d=drift, f=f: (x0 + d * u * f, top - (top + 5) * u * f), t, b, "linear")
            t = b

def Snow(n=60, start=0, end=100, color="white", seed=0, speed=(35, 70)):
    """n snowflakes falling from start to end (speed = frames per fall)."""
    _particles("snow", n, start, end, seed, color, speed)

def Rain(n=90, start=0, end=100, color="#9ecbff", seed=0, speed=(8, 14)):
    _particles("rain", n, start, end, seed, color, speed)

def Flash(start=0, end=6, color="white"):
    """Lightning: the whole screen flashes and fades."""
    f = DrawRect(color, 50, -5, w=140, h=75, alpha=0, z=50)
    f.hud = True
    Fade(f, .85, start, start + 2)
    Fade(f, 0, start + 2, end)
    return f

# ---------- dialogue and cast ----------
def Talk(shape, text, start=0, end=40, color="black"):
    """Speech bubble above `shape` from frame start to end. It follows the shape."""
    b = Bubble(shape, text, _s(), color, alpha=0)
    _s().add(b)
    Fade(b, 1, start, start + 2)
    Fade(b, 0, max(start + 3, end - 2), end)
    return b

def Dialogue(T, lines, start=0.5, pause=0.3):
    """Bubbles one after another. T converts seconds to frames. lines = [(shape, text), ...].
    Returns the time (seconds) when the last line ends, so you can start the next action there."""
    t = start
    for shape, text in lines:
        d = max(1.6, 0.07 * len(text))
        Talk(shape, text, T(t), T(t + d))
        t += d + pause
    return t

class Cast:
    """Recurring characters: cast = Cast(Mia=("Person", "orchid", 0.7)); mia = cast.Mia(30, 11)."""
    def __init__(self, **chars):
        self._c = chars
    def __getattr__(self, name):
        c = self.__dict__.get("_c", {})
        if name not in c: raise AttributeError(name)
        kind, color, size = (tuple(c[name]) + (1,))[:3]
        def make(x, y, **kw):
            sh = DrawShape(kind, color, x, y, kw.pop("size", size), **kw)
            sh.name = name
            return sh
        return make

# ---------- catalogue of 1,000+ shapes, SVG import ----------
def Shapes(kind=None):
    """All shape names. Shapes('star') lists only names starting with 'star'."""
    names = sorted(CATALOG) + sorted(SHAPES)
    return [n for n in names if kind is None or n.lower().startswith(kind.lower())]

def Find(word):
    """Names containing `word`: Find('flower')."""
    w = word.lower()
    return [n for n in Shapes() if w in n.lower()]

def _hsv(rng):
    from matplotlib.colors import hsv_to_rgb
    return tuple(hsv_to_rgb((rng.random(), .6 + .3 * rng.random(), .75 + .25 * rng.random())))

def DrawShape(name, color, x, y, size=1, **kw):
    """DrawShape('star_5_thin', 'gold', 50, 30). color='random' picks a pleasant colour."""
    if color == "random": color = _hsv(random.Random(zlib.crc32(name.encode())))
    if name in SHAPES: return globals()["Draw" + name](color, x, y, size, **kw)
    if name not in CATALOG:
        raise KeyError("unknown shape %r, try Find(%r)" % (name, name.split("_")[0]))
    kind, params = CATALOG[name]
    return _s().add(Procedural(kind, params, color, x, y, size, **kw))

def RandomShape(x, y, size=1, seed=None, color=None):
    r = random.Random(seed)
    return DrawShape(r.choice(sorted(CATALOG)), color or _hsv(r), x, y, size)

def DrawSVG(src, x, y, size=1, width=10, color=None, **kw):
    """Import an SVG icon: DrawSVG('heart.svg', 50, 20, width=10). Needs pip install svgpath2mpl."""
    return _s().add(SvgShape(src, x, y, size, width=width, color=color, **kw))

# ---------- output ----------
def Show(t=0):                                          _s().show(t)
def Save(path="scene.gif", fps=20, hold=0, show=True):  return _s().save(path, fps, hold, show)
def Filmstrip(n=6):                                     return _s().filmstrip(n)
def Frames():                                           return _s().frames()

def Gallery():
    """Draw every hand-made shape with its name, to check the install."""
    sc = NewScene("plain", ground_h=0)
    colors = ["tomato", "royalblue", "gold", "seagreen", "orchid", "darkorange", "teal"]
    for i, (name, cls) in enumerate(SHAPES.items()):
        col, row = i % 10, i // 10
        x, base = 5 + col * 10, 44 - row * 19
        sc.add(cls(colors[i % len(colors)], x, base + (5 if cls.origin == "center" else 0), 0.55))
        sc.add(Label("black", x, base - 3.5, 0.5, text=name))
    sc.show()
    return sc

def Sheet(prefix="", n=60, cols=10, color="royalblue", width_px=1100):
    """Picture grid of catalogue shapes whose names start with `prefix` (evenly sampled if more than n)."""
    names = [k for k in sorted(CATALOG) if k.startswith(prefix)]
    if not names: raise ValueError("no shapes start with %r" % prefix)
    if len(names) > n: names = [names[int(i * len(names) / n)] for i in range(n)]
    cw = 100 / cols; ch = cw * 1.05
    rows = -(-len(names) // cols); H = rows * ch + 2
    sc = NewScene("plain", w=100, h=H, ground_h=0, width_px=width_px)
    for i, name in enumerate(names):
        c, r = i % cols, i // cols
        x, y = cw * (c + .5), H - ch * (r + .5)
        DrawShape(name, color, x, y + .6, size=cw / 12)
        DrawText(name, "black", x, y - cw * .5, 1, fontsize=5)
    sc.show()
    return sc
