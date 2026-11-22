import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.patches import Rectangle, Ellipse
from matplotlib.colors import to_rgb
from PIL import Image
from . import easing

THEMES = {
    "day":    dict(bg=("#3d9be0", "#d4ecff"), ground="#3a9d5d"),
    "sunset": dict(bg=("#3b2667", "#ff9966"), ground="#2f6b3f"),
    "night":  dict(bg=("#04081f", "#1c2d63"), ground="#1c4a2b"),
    "plain":  dict(bg="#dfe7ef", ground=None),
}
SHADOW_W = {"Car": 16, "Person": 5, "House": 16, "Tree": 9, "Pine": 9, "Cube": 8,
            "Ball": 4, "Boat": 12, "Rocket": 7, "Fence": 11, "Mountain": 26}

class Camera:
    def __init__(self, w, h):
        self.x, self.y, self.zoom = w / 2, h / 2, 1.0
        self._init = self.state(); self._plan = dict(self._init)
    def state(self): return dict(x=self.x, y=self.y, zoom=self.zoom)
    def reset(self):
        for k, v in self._init.items(): setattr(self, k, v)
    def set(self, prop, v):
        if prop == "xy": self.x, self.y = v
        else: setattr(self, prop, v)

class Scene:
    def __init__(self, theme="day", w=100, h=60, bg=None, ground=None, ground_h=18, width_px=800, depth_k=0.25):
        t = THEMES[theme]
        self.w, self.h, self.gh, self.width_px, self.depth_k = w, h, ground_h, width_px, depth_k
        self.bg = bg if bg is not None else t["bg"]
        self.ground = ground if ground is not None else t["ground"]
        self.shapes, self.tracks, self.follows = [], [], []
        self.camera = Camera(w, h)

    def add(self, shape):
        self.shapes.append(shape); return shape

    def track(self, shape, prop, fn, start, end, ease="ease", mode="set"):
        self.tracks.append(dict(shape=shape, prop=prop, fn=fn, start=start, end=end,
                                ease=easing.get(ease), mode=mode))

    def n_frames(self, hold=0):
        return int(max([t["end"] for t in self.tracks] + [0])) + 1 + hold

    def _run(self, mode, t):
        for tr in sorted((r for r in self.tracks if r["mode"] == mode), key=lambda r: r["start"]):
            if t < tr["start"]: continue
            span = tr["end"] - tr["start"]
            u = 1.0 if span <= 0 or t >= tr["end"] else (t - tr["start"]) / span
            v = tr["fn"](tr["ease"](u))
            s = tr["shape"]
            s.set(tr["prop"], getattr(s, tr["prop"]) + v if mode == "add" else v)

    def _apply(self, t):
        for s in self.shapes + [self.camera]: s.reset()
        self._run("set", t)
        for fo in self.follows:
            if t >= fo["start"]:
                self.camera.x = fo["shape"].x + fo["offset"][0]
                if fo["axis"] == "xy": self.camera.y = fo["shape"].y + fo["offset"][1]
        for s in self.shapes: s._gy = s.y           # ground height before hops (for shadows)
        self._run("add", t)

    def _persp(self, s):
        return 1.0 / (1.0 + max(s.depth, -2.0) * self.depth_k)

    def _screen_y(self, y, f):
        c = self.camera
        wy = self.gh + (y - self.gh) * f             # converge toward the horizon with distance
        return self.h / 2 + (wy - c.y) * c.zoom

    def _project(self, s):
        """world -> (screen x, screen y, screen size, perspective factor)"""
        if getattr(s, "hud", False): return s.x, s.y, s.size, 1.0
        c, f = self.camera, self._persp(s)
        return (self.w / 2 + (s.x - c.x) * f * c.zoom, self._screen_y(s.y, f), s.size * f * c.zoom, f)

    def frame(self, t=0):
        self._apply(t)
        pw = self.width_px; ph = int(round(pw * self.h / self.w))
        fig = Figure(figsize=(pw / 100, ph / 100), dpi=100)
        canvas = FigureCanvasAgg(fig)
        ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
        if isinstance(self.bg, (tuple, list)):
            top, bot = np.array(to_rgb(self.bg[0])), np.array(to_rgb(self.bg[1]))
            k = np.linspace(0, 1, 128)[:, None, None]
            ax.imshow(top * (1 - k) + bot * k, extent=(0, self.w, 0, self.h), aspect="auto", zorder=0)
        else:
            ax.add_patch(Rectangle((0, 0), self.w, self.h, color=self.bg, zorder=0))
        if self.ground and self.gh > 0:
            gy = self._screen_y(self.gh, 1.0)
            ax.add_patch(Rectangle((0, -3 * self.h), self.w, gy + 3 * self.h, color=self.ground, zorder=0.5))
        for s in sorted(self.shapes, key=lambda s: (-s.depth, s.z)):
            sx, sy, ss, f = self._project(s)
            m = 30 * max(ss, 1.0)
            if sx < -m or sx > self.w + m: continue
            if s.shadow and s.alpha > 0:
                gyw = getattr(s, "_gy", s.y)
                lift = max(s.y - gyw, 0.0)
                wdt = SHADOW_W.get(type(s).__name__, 8) * ss / (1 + lift * 0.15)
                ax.add_patch(Ellipse((sx, self._screen_y(gyw, f)), wdt, wdt * 0.2,
                                     color="black", alpha=0.25 * s.alpha, zorder=0.9))
            ox, oy, osz = s.x, s.y, s.size
            s.x, s.y, s.size = sx, sy, ss
            s.draw(ax)
            s.x, s.y, s.size = ox, oy, osz
        ax.set_xlim(0, self.w); ax.set_ylim(0, self.h)
        canvas.draw()
        return np.asarray(canvas.buffer_rgba())[..., :3].copy()

    def frames(self, hold=0):
        return [self.frame(t) for t in range(self.n_frames(hold))]

    def show(self, t=0):
        from IPython.display import display
        display(Image.fromarray(self.frame(t)))

    def save(self, path="scene.gif", fps=20, hold=0, show=True):
        if path.lower().endswith(".png"):
            Image.fromarray(self.frame(0)).save(path)
        elif path.lower().endswith(".gif"):
            imgs = [Image.fromarray(f) for f in self.frames(hold)]
            imgs[0].save(path, save_all=True, append_images=imgs[1:],
                         duration=max(20, int(1000 / fps)), loop=0)
        else:
            raise ValueError("use a .gif or .png path")
        if show:
            from IPython.display import Image as IPImage, display
            display(IPImage(path))
        return path

    def filmstrip(self, n=6, width=260):
        total = self.n_frames()
        ts = [round(i * (total - 1) / max(n - 1, 1)) for i in range(n)]
        ims = [Image.fromarray(self.frame(t)) for t in ts]
        ims = [im.resize((width, int(im.height * width / im.width))) for im in ims]
        strip = Image.new("RGB", (width * n + 4 * (n - 1), ims[0].height), "white")
        for i, im in enumerate(ims): strip.paste(im, (i * (width + 4), 0))
        from IPython.display import display
        display(strip)
        return strip
