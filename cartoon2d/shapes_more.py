import math, os, random
from matplotlib.patches import Polygon, Circle, Ellipse, Wedge, PathPatch
from matplotlib.colors import to_rgb
from .shapes import Shape, dark, light, _bar

def _ring(rs, a0=math.pi / 2):
    n = len(rs)
    return [(r * math.cos(a0 + 2 * math.pi * i / n), r * math.sin(a0 + 2 * math.pi * i / n))
            for i, r in enumerate(rs)]

def _shade(c, k):
    return dark(c, k) if k <= 1 else light(c, k - 1)

class Procedural(Shape):
    """A shape built by a generator: kind + params (see CATALOG). Centred on (x, y), radius about 5."""
    origin = "center"
    def __init__(self, kind, params, color, x, y, size=1, **kw):
        self.kind, self.params = kind, dict(params)
        super().__init__(color, x, y, size, **kw)
    def parts(self):
        return getattr(self, "_" + self.kind)(self.color, **self.params)

    def _polygon(self, c, n):
        return [Polygon(_ring([5] * n), color=c)]
    def _star(self, c, n, inner):
        return [Polygon(_ring([5 if i % 2 == 0 else 5 * inner for i in range(2 * n)]), color=c)]
    def _gear(self, c, n):
        rs = [5.4 if i % 4 in (0, 1) else 4.3 for i in range(4 * n)]
        return [Polygon(_ring(rs, 0), color=c), Circle((0, 0), 1.8, color=dark(c, .55)),
                Circle((0, 0), 0.8, color=light(c, .5))]
    def _blob(self, c, seed):
        r = random.Random(seed)
        ph = [r.uniform(0, 6.28) for _ in range(4)]
        am = [r.uniform(.3, .9) / (k + 1) for k in range(4)]
        rs = [4 + sum(am[j] * math.sin((j + 2) * th + ph[j]) for j in range(4))
              for th in (2 * math.pi * i / 60 for i in range(60))]
        return [Polygon(_ring(rs), color=c), Circle((-1.3, 1.4), 0.9, color=light(c, .5))]
    def _rock(self, c, seed):
        r = random.Random(seed)
        pts = _ring([r.uniform(3.2, 5) for _ in range(r.randint(6, 10))], r.uniform(0, 6.28))
        return [Polygon(pts, color=dark(c, .8)), Polygon([(0, 0)] + pts[:3], color=light(c, .25))]
    def _flower(self, c, n, style):
        L, Wd = {"round": (3.0, 3.0), "long": (4.6, 1.7), "wide": (3.6, 2.8)}[style]
        out = []
        for i in range(n):
            a = 2 * math.pi * i / n
            out.append(Ellipse((3 * math.cos(a), 3 * math.sin(a)), L, Wd, angle=math.degrees(a), color=c))
        out.append(Circle((0, 0), 1.5, color="#ffd54f"))
        return out
    def _burst(self, c, n):
        return [Polygon(_ring([5 if i % 2 == 0 else 2.8 for i in range(2 * n)]), color=c),
                Circle((0, 0), 2.6, color=light(c, .5))]
    def _cross(self, c, n):
        return [_bar(0, 0, 10.5, 1.7, math.pi / 2 + math.pi * i / n, c) for i in range(n)] + \
               [Circle((0, 0), 1.4, color=dark(c, .6))]
    def _pie(self, c, n):
        return [Wedge((0, 0), 5, 360 * i / n, 360 * (i + 1) / n, color=c if i % 2 == 0 else light(c, .5))
                for i in range(n)]
    def _snowflake(self, c, arms, seed):
        r = random.Random(seed)
        br = [(r.uniform(.25, .8), r.uniform(1.0, 2.2)) for _ in range(r.randint(2, 3))]
        out = []
        for i in range(arms):
            a = math.pi / 2 + 2 * math.pi * i / arms
            out.append(_bar(2.6 * math.cos(a), 2.6 * math.sin(a), 5.2, 0.55, a, c))
            for t, L in br:
                bx, by = 5 * t * math.cos(a), 5 * t * math.sin(a)
                for s in (-1, 1):
                    ba = a + s * math.pi / 3
                    out.append(_bar(bx + L / 2 * math.cos(ba), by + L / 2 * math.sin(ba), L, 0.45, ba, c))
        out.append(Circle((0, 0), 0.8, color=c))
        return out
    def _crystal(self, c, seed):
        r = random.Random(seed); n = r.randint(6, 9)
        pts = _ring([r.uniform(3.4, 5) for _ in range(n)], r.uniform(0, 6.28))
        return [Polygon([(0, 0), pts[i], pts[(i + 1) % n]], color=_shade(c, .55 + .9 * r.random()))
                for i in range(n)]
    def _puff(self, c, seed):
        r = random.Random(seed)
        out = [Circle((r.uniform(-3, 3), r.uniform(-1.5, 1.5)), r.uniform(1.6, 2.6), color=c)
               for _ in range(r.randint(4, 7))]
        out.append(Circle((r.uniform(-1, 1), 1.2), 1.0, color=light(c, .5)))
        return out
    def _mandala(self, c, seed):
        r = random.Random(seed); L = r.randint(3, 5); out = []
        for i in range(L):
            rad, n, inner = 5 * (1 - i / L), r.randint(5, 12), r.choice([1.0, .8, .6, .45])
            rs = [rad if j % 2 == 0 else rad * inner for j in range(2 * n)]
            out.append(Polygon(_ring(rs, r.uniform(0, 3.14)), color=_shade(c, .7 if i % 2 == 0 else 1.3)))
        out.append(Circle((0, 0), 0.7, color="white"))
        return out
    def _heart(self, c):
        pts = []
        for i in range(60):
            t = 2 * math.pi * i / 60
            x = 16 * math.sin(t) ** 3
            y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
            pts.append((0.3 * x, 0.3 * (y + 2.5)))
        return [Polygon(pts, color=c)]
    def _bolt(self, c):
        return [Polygon([(1, 5), (-3, -0.5), (-0.3, -0.5), (-1.5, -5.5), (3, 1), (0.4, 1)], color=c)]
    def _arrow(self, c):
        return [Polygon([(-5, -1.5), (1, -1.5), (1, -3.5), (5.5, 0), (1, 3.5), (1, 1.5), (-5, 1.5)], color=c)]

CATALOG = {}
def _build():
    def R(name, kind, **p): CATALOG[name] = (kind, p)
    for n in range(3, 41): R("polygon_%d" % n, "polygon", n=n)
    for n in range(3, 25):
        for tag, k in (("fat", .65), ("mid", .5), ("thin", .35)): R("star_%d_%s" % (n, tag), "star", n=n, inner=k)
    for n in range(5, 31): R("gear_%d" % n, "gear", n=n)
    for i in range(300): R("blob_%d" % i, "blob", seed=i)
    for i in range(150): R("rock_%d" % i, "rock", seed=i)
    for n in range(3, 21):
        for st in ("round", "long", "wide"): R("flower_%d_%s" % (n, st), "flower", n=n, style=st)
    for n in range(6, 41): R("burst_%d" % n, "burst", n=n)
    for n in range(2, 13): R("cross_%d" % n, "cross", n=n)
    for n in range(2, 17): R("pie_%d" % n, "pie", n=n)
    for arms in range(4, 13):
        for s in range(10): R("snowflake_%d_%d" % (arms, s), "snowflake", arms=arms, seed=s)
    for i in range(100):
        R("crystal_%d" % i, "crystal", seed=i); R("puff_%d" % i, "puff", seed=i); R("mandala_%d" % i, "mandala", seed=i)
    for k in ("heart", "bolt", "arrow"): R(k, k)
_build()

class SvgShape(Shape):
    """An SVG icon as a shape (reads <path> fills only). Bottom-centre origin."""
    def __init__(self, src, x, y, size=1, width=10, color=None, **kw):
        import xml.etree.ElementTree as ET
        from svgpath2mpl import parse_path
        from matplotlib.transforms import Affine2D
        txt = open(src).read() if os.path.exists(src) else src
        root = ET.fromstring(txt)
        vb = root.get("viewBox")
        if vb: vx, vy, vw, vh = [float(v) for v in vb.replace(",", " ").split()]
        else:
            vx = vy = 0.0
            vw, vh = [float(str(root.get(k, "100")).replace("px", "")) for k in ("width", "height")]
        s = width / vw
        aff = Affine2D().translate(-(vx + vw / 2), -(vy + vh)).scale(s, -s)
        self._items = []
        for el in root.iter():
            if not el.tag.endswith("path") or not el.get("d"): continue
            fill = el.get("fill")
            for part in (el.get("style") or "").split(";"):
                if part.strip().startswith("fill:"): fill = part.split(":", 1)[1].strip()
            if fill == "none": continue
            col = color if color is not None else fill
            try: col = to_rgb(col) if col and col != "currentColor" else to_rgb(color or "black")
            except ValueError: col = (0, 0, 0)
            self._items.append((parse_path(el.get("d")).transformed(aff), col))
        if not self._items: raise ValueError("no fillable <path> found in the SVG")
        super().__init__(color, x, y, size, **kw)
    def parts(self):
        return [PathPatch(p, facecolor=c, edgecolor="none") for p, c in self._items]
