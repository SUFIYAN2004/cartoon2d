import os, re, shutil, subprocess, time
from . import api

__all__ = ["Episode"]

class Episode:
    """A long video made of scenes. Each scene streams to its own mp4, then the parts are joined."""
    def __init__(self, title, fps=15, width_px=480, theme="day"):
        self.title, self.fps, self.width_px, self.theme = title, fps, width_px, theme
        self.scenes = []

    def scene(self, name, seconds=10, theme=None, **kw):
        """Decorator. The function gets T (seconds -> frames): def park(T): Move(x, (90, 5), T(0), T(4))"""
        def deco(fn):
            self.scenes.append(dict(name=name, seconds=seconds, theme=theme or self.theme, kw=kw, fn=fn))
            return fn
        return deco

    def card(self, text, seconds=3, bg="#101820", color="white", size=1.4):
        def fn(T): api.DrawText(text, color, 50, 30, size)
        self.scenes.append(dict(name="card", seconds=seconds, theme="plain", kw=dict(bg=bg, ground_h=0), fn=fn))

    def duration(self):
        return sum(s["seconds"] for s in self.scenes)

    def _build(self, spec):
        sc = api.NewScene(spec["theme"], width_px=self.width_px, **spec["kw"])
        fps = self.fps
        T = lambda sec: int(round(sec * fps))
        n = T(spec["seconds"])
        spec["fn"](T)
        sc.length = n
        k = api.DrawRect("black", 50, -5, w=140, h=75, z=100)      # fade in / out
        k.hud = True
        api.Fade(k, 0, 0, T(0.4))
        api.Fade(k, 1, max(n - 1 - T(0.4), T(0.4)), n - 1)
        return sc

    def preview(self, i=0, n=6):
        return self._build(self.scenes[i]).filmstrip(n)

    def estimate(self, samples=6):
        assert self.scenes, "no scenes yet"
        sc = self._build(max(self.scenes, key=lambda s: s["seconds"]))
        n = sc.n_frames(); t0 = time.time()
        for i in range(samples): sc.frame(int(i * (n - 1) / max(samples - 1, 1)))
        per = (time.time() - t0) / samples
        frames = int(round(self.duration() * self.fps))
        print("%.2f s/frame x %d frames = about %.1f min to render (%.1f min of video)"
              % (per, frames, per * frames / 60, self.duration() / 60))
        return per * frames

    def render(self, out=None, only=None, workdir="_episode", resume=False):
        if shutil.which("ffmpeg") is None: raise RuntimeError("ffmpeg not found")
        out = out or re.sub(r"\W+", "_", self.title.lower()).strip("_") + ".mp4"
        os.makedirs(workdir, exist_ok=True)
        idx = list(range(len(self.scenes))) if only is None else list(only)
        parts, t0 = [], time.time()
        for i in idx:
            spec = self.scenes[i]
            part = os.path.join(workdir, "scene_%03d.mp4" % i)
            if resume and os.path.exists(part) and os.path.getsize(part) > 0:
                print("[%d/%d] %s: reusing" % (i + 1, len(self.scenes), spec["name"]))
            else:
                print("[%d/%d] %s (%.0fs)..." % (i + 1, len(self.scenes), spec["name"], spec["seconds"]), flush=True)
                tmp = part[:-4] + ".tmp.mp4"
                self._build(spec).save(tmp, self.fps, 0, False)
                os.replace(tmp, part)
            parts.append(part)
        lst = os.path.join(workdir, "list.txt")
        with open(lst, "w") as f:
            for p in parts: f.write("file '%s'\n" % os.path.abspath(p).replace("'", "'\\''"))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                        "-i", lst, "-c", "copy", out], check=True)
        print("wrote %s in %.1f min" % (out, (time.time() - t0) / 60))
        return out
