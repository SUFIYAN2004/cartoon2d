import math
from matplotlib.patches import Rectangle, Circle, Polygon, Ellipse
from matplotlib.transforms import Affine2D
from matplotlib.colors import to_rgb

__all__ = ["Shape", "Car", "Sun", "Moon", "Star", "House", "Tree", "Pine", "Cloud", "Mountain",
           "Flower", "Fence", "Person", "Bird", "Boat", "Balloon", "Rocket", "Fish", "Ball",
           "Rect", "Disc", "Triangle", "Label", "dark", "light"]

def dark(c, k=0.7):
    r, g, b = to_rgb(c); return (r * k, g * k, b * k)
def light(c, k=0.5):
    r, g, b = to_rgb(c); return (r + (1 - r) * k, g + (1 - g) * k, b + (1 - b) * k)

class Shape:
    """Local coordinates: origin = bottom-centre (or centre if origin == 'center'), y up."""
    origin = "bottom"
    def __init__(self, color, x, y, size=1, alpha=1.0, rot=0.0, flip=False, z=0, depth=0.0, shadow=False):
        self.color, self.x, self.y, self.size = color, x, y, size
        self.alpha, self.rot, self.flip, self.z = alpha, rot, flip, z
        self.depth, self.shadow, self.phase = depth, shadow, 0.0
        self._init = self.state()
        self._plan = dict(self._init)       # where the last animation ends (for chaining)
    def state(self):
        return dict(x=self.x, y=self.y, size=self.size, rot=self.rot, alpha=self.alpha, depth=self.depth, phase=self.phase)
    def reset(self):
        for k, v in self._init.items(): setattr(self, k, v)
    def set(self, prop, v):
        if prop == "xy": self.x, self.y = v
        else: setattr(self, prop, v)
    def parts(self): raise NotImplementedError
    def draw(self, ax):
        if self.alpha <= 0: return
        sx = -self.size if self.flip else self.size
        tr = Affine2D().scale(sx, self.size).rotate_deg(self.rot).translate(self.x, self.y) + ax.transData
        for p in self.parts():
            p.set_transform(tr); p.set_alpha(self.alpha); ax.add_patch(p)

class Car(Shape):
    def parts(self):
        c = self.color
        out = [Rectangle((-7, 2), 14, 3.5, color=c),
               Polygon([(-4, 5.5), (-2, 9), (3, 9), (5, 5.5)], color=c),
               Polygon([(-3.3, 5.8), (-2.2, 8.3), (-0.2, 8.3), (-0.2, 5.8)], color="#cfe8ff"),
               Polygon([(0.3, 5.8), (0.3, 8.3), (2.4, 8.3), (3.6, 5.8)], color="#cfe8ff"),
               Circle((6.6, 4), 0.6, color="#ffe066")]
        for wx in (-3.5, 3.5):
            out += [Circle((wx, 2), 1.8, color="black"), Circle((wx, 2), 0.7, color="#bbbbbb")]
        return out

class Sun(Shape):
    origin = "center"
    def parts(self):
        c = self.color
        out = [Circle((0, 0), 6, color=c)]
        for i in range(12):
            a = math.radians(i * 30)
            out.append(Polygon([(7.2 * math.cos(a - .14), 7.2 * math.sin(a - .14)),
                                (10.5 * math.cos(a), 10.5 * math.sin(a)),
                                (7.2 * math.cos(a + .14), 7.2 * math.sin(a + .14))], color=c))
        return out

class Moon(Shape):
    origin = "center"
    def parts(self):
        c = self.color
        return [Circle((0, 0), 6, color=c), Circle((-2, 1.5), 1.2, color=dark(c, .85)),
                Circle((2, -2), 0.8, color=dark(c, .85)), Circle((1.5, 3), 0.6, color=dark(c, .85))]

class Star(Shape):
    origin = "center"
    def parts(self):
        pts = [((5 if i % 2 == 0 else 2) * math.cos(math.pi / 2 + i * math.pi / 5),
                (5 if i % 2 == 0 else 2) * math.sin(math.pi / 2 + i * math.pi / 5)) for i in range(10)]
        return [Polygon(pts, color=self.color)]

class House(Shape):
    def parts(self):
        c = self.color
        return [Rectangle((4, 12), 1.6, 4, color="#5d4037"),
                Rectangle((-7, 0), 14, 10, color=c),
                Polygon([(-8.5, 10), (0, 17), (8.5, 10)], color="#7a3b1e"),
                Rectangle((-1.5, 0), 3, 5, color="#4a2a14"),
                Rectangle((-5.5, 5), 3, 3, color="#cfe8ff"), Rectangle((2.5, 5), 3, 3, color="#cfe8ff")]

class Tree(Shape):
    def parts(self):
        c = self.color
        return [Rectangle((-1, 0), 2, 7, color="#6b4423"), Circle((0, 10), 5, color=c),
                Circle((-3, 8.5), 3.5, color=c), Circle((3, 8.5), 3.5, color=c)]

class Pine(Shape):
    def parts(self):
        c = self.color
        return [Rectangle((-0.8, 0), 1.6, 4, color="#6b4423"),
                Polygon([(-5, 3), (0, 10), (5, 3)], color=c),
                Polygon([(-4, 6.5), (0, 13), (4, 6.5)], color=c),
                Polygon([(-3, 10), (0, 16), (3, 10)], color=c)]

class Cloud(Shape):
    origin = "center"
    def parts(self):
        return [Ellipse((dx, dy), w, 5, color=self.color) for dx, dy, w in [(0, 0, 10), (4, 2, 8), (-4, 1.5, 7)]]

class Mountain(Shape):
    def parts(self):
        return [Polygon([(-14, 0), (0, 20), (14, 0)], color=self.color),
                Polygon([(-3.5, 14.2), (0, 20), (3.5, 14.2), (1.5, 13), (0, 14.5), (-1.5, 13)], color="white")]

class Flower(Shape):
    def parts(self):
        out = [Rectangle((-0.25, 0), 0.5, 5, color="#2e7d32")]
        for i in range(6):
            a = math.radians(i * 60)
            out.append(Circle((1.3 * math.cos(a), 5 + 1.3 * math.sin(a)), 1.0, color=self.color))
        out.append(Circle((0, 5), 0.9, color="#ffd54f"))
        return out

class Fence(Shape):
    def parts(self):
        c = self.color
        out = [Rectangle((-5.4, 1), 10.8, 0.5, color=c), Rectangle((-5.4, 2.8), 10.8, 0.5, color=c)]
        out += [Rectangle((x - 0.4, 0), 0.8, 4, color=c) for x in (-5, -2.5, 0, 2.5, 5)]
        return out

class Person(Shape):
    def parts(self):
        c, skin = self.color, "#f1c27d"
        return [Rectangle((-1.6, 0), 1.3, 6, color="#333333"), Rectangle((0.3, 0), 1.3, 6, color="#333333"),
                Rectangle((-3.2, 6.5), 1.2, 5, color=dark(c, .8)), Rectangle((2, 6.5), 1.2, 5, color=dark(c, .8)),
                Rectangle((-1.8, 6), 3.6, 6, color=c),
                Circle((0, 14), 2, color=skin), Ellipse((0, 15.3), 4, 1.5, color="#3b2a1a")]

class Bird(Shape):
    origin = "center"
    def parts(self):
        c = self.color
        return [Polygon([(-2, 0), (-4, 0.8), (-3.8, -0.6)], color=c), Ellipse((0, 0), 4, 2, color=c),
                Polygon([(-0.5, 0.5), (-2, 3), (1, 0.5)], color=dark(c, .6)), Circle((2, 0.6), 0.9, color=c),
                Polygon([(2.8, 0.6), (3.8, 0.3), (2.8, 0.1)], color="orange")]

class Boat(Shape):
    def parts(self):
        return [Rectangle((-0.2, 2), 0.4, 9, color="#6b4423"),
                Polygon([(0.5, 3), (0.5, 10.5), (5, 3)], color="white"),
                Polygon([(-0.5, 3), (-0.5, 9), (-4, 3)], color="#f4f4f4"),
                Polygon([(-6, 2), (6, 2), (4, -1), (-4, -1)], color=self.color)]

class Balloon(Shape):
    def parts(self):
        c = self.color
        return [Rectangle((-1.2, 2.4), 2.4, 2.2, color="#8d5524"), Ellipse((0, 9), 8, 9, color=c),
                Ellipse((0, 9), 3, 9, color=light(c, .5))]

class Rocket(Shape):
    def parts(self):
        return [Polygon([(-1.2, 2), (0, -2.5), (1.2, 2)], color="#ffa000"),
                Polygon([(-2, 2), (-4.5, 0), (-2, 5)], color="#e53935"),
                Polygon([(2, 2), (4.5, 0), (2, 5)], color="#e53935"),
                Rectangle((-2, 2), 4, 10, color=self.color),
                Polygon([(-2, 12), (0, 17), (2, 12)], color="#e53935"),
                Circle((0, 8), 1.1, color="#cfe8ff")]

class Fish(Shape):
    origin = "center"
    def parts(self):
        c = self.color
        return [Polygon([(-2.6, 0), (-4.8, 1.8), (-4.8, -1.8)], color=c), Ellipse((0, 0), 6, 3.2, color=c),
                Circle((1.6, 0.4), 0.45, color="white"), Circle((1.7, 0.4), 0.2, color="black")]

class Ball(Shape):
    def parts(self):
        return [Circle((0, 2), 2, color=self.color), Circle((-0.7, 2.8), 0.6, color=light(self.color, .7))]

class Rect(Shape):
    def __init__(self, color, x, y, size=1, w=10, h=5, **kw):
        self.w, self.h = w, h
        super().__init__(color, x, y, size, **kw)
    def parts(self): return [Rectangle((-self.w / 2, 0), self.w, self.h, color=self.color)]

class Disc(Shape):
    origin = "center"
    def __init__(self, color, x, y, size=1, r=3, **kw):
        self.r = r
        super().__init__(color, x, y, size, **kw)
    def parts(self): return [Circle((0, 0), self.r, color=self.color)]

class Triangle(Shape):
    def __init__(self, color, x, y, size=1, w=10, h=8, **kw):
        self.w, self.h = w, h
        super().__init__(color, x, y, size, **kw)
    def parts(self): return [Polygon([(-self.w / 2, 0), (self.w / 2, 0), (0, self.h)], color=self.color)]

class Label(Shape):
    origin = "center"
    def __init__(self, color, x, y, size=1, text="Hello", fontsize=16, **kw):
        self.text, self.fontsize = text, fontsize
        super().__init__(color, x, y, size, **kw)
    def draw(self, ax):
        if self.alpha <= 0: return
        ax.text(self.x, self.y, self.text, color=self.color, fontsize=self.fontsize * self.size,
                ha="center", va="center", rotation=self.rot, alpha=self.alpha, fontweight="bold", zorder=10)
# ---------------- v0.3 additions ----------------
Shape.hud = False

def _bar(cx, cy, length, width, angle, color):
    dx, dy = math.cos(angle) * length / 2, math.sin(angle) * length / 2
    px, py = -math.sin(angle) * width / 2, math.cos(angle) * width / 2
    return Polygon([(cx - dx - px, cy - dy - py), (cx + dx - px, cy + dy - py),
                    (cx + dx + px, cy + dy + py), (cx - dx + px, cy - dy + py)], color=color)

def _limb(x, y, length, width, swing, color):
    ex, ey = x + length * math.sin(swing), y - length * math.cos(swing)
    return _bar((x + ex) / 2, (y + ey) / 2, length, width, math.atan2(ey - y, ex - x), color)

class Car(Shape):
    def parts(self):
        c = self.color
        out = [Rectangle((-7, 2), 14, 3.5, color=c),
               Polygon([(-4, 5.5), (-2, 9), (3, 9), (5, 5.5)], color=c),
               Polygon([(-3.3, 5.8), (-2.2, 8.3), (-0.2, 8.3), (-0.2, 5.8)], color="#cfe8ff"),
               Polygon([(0.3, 5.8), (0.3, 8.3), (2.4, 8.3), (3.6, 5.8)], color="#cfe8ff"),
               Circle((6.6, 4), 0.6, color="#ffe066")]
        for wx in (-3.5, 3.5):
            out += [Circle((wx, 2), 1.8, color="black"), Circle((wx, 2), 1.25, color="#b0b0b0")]
            out += [_bar(wx, 2, 2.5, 0.28, self.phase + k * math.pi / 3, "#555555") for k in range(3)]
            out.append(Circle((wx, 2), 0.35, color="#333333"))
        return out

class Person(Shape):
    def parts(self):
        c, skin = self.color, "#f1c27d"
        sw = 0.55 * math.sin(self.phase)
        return [_limb(-0.95, 6, 6, 1.3, sw, "#333333"), _limb(0.95, 6, 6, 1.3, -sw, "#333333"),
                _limb(-2.4, 11.6, 5, 1.2, -0.8 * sw, dark(c, .8)), _limb(2.4, 11.6, 5, 1.2, 0.8 * sw, dark(c, .8)),
                Rectangle((-1.8, 6), 3.6, 6, color=c),
                Circle((0, 14), 2, color=skin), Ellipse((0, 15.3), 4, 1.5, color="#3b2a1a")]

class Cube(Shape):
    """A real rotating cube: 3D corners, yaw = phase, tilted 30 degrees toward the viewer."""
    def parts(self):
        s, e, h = 6.0, math.radians(30), 3.0
        th = self.phase + 0.6
        cs, sn = math.cos(th), math.sin(th)
        base = [(X * cs - Z * sn, X * sn + Z * cs) for X, Z in [(-h, -h), (h, -h), (h, h), (-h, h)]]
        def P(i, Y):
            X, Z = base[i]
            return (X, Y * math.cos(e) + Z * math.sin(e) + 2.2)
        out = []
        for i in range(4):
            j = (i + 1) % 4
            mx, mz = (base[i][0] + base[j][0]) / 2, (base[i][1] + base[j][1]) / 2
            n = math.hypot(mx, mz); nx, nz = mx / n, mz / n
            if nz >= 0: continue                                   # faces away from the viewer
            k = 0.6 + 0.4 * max(0.0, -0.6 * nx - 0.8 * nz)         # simple lighting
            out.append(Polygon([P(i, 0), P(j, 0), P(j, s), P(i, s)], color=dark(self.color, k)))
        out.append(Polygon([P(i, s) for i in range(4)], color=light(self.color, .3)))
        return out

class Sphere(Shape):
    origin = "center"
    def parts(self):
        c = self.color; lo, hi = dark(c, .65), light(c, .65)
        out = []
        for i in range(7):
            t = i / 6
            col = tuple(a * (1 - t) + b * t for a, b in zip(lo, hi))
            out.append(Circle((-1.2 * t, 1.6 * t), 6 * (1 - 0.82 * t), color=col))
        return out

__all__ += ["Cube", "Sphere"]
