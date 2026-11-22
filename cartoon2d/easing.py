def linear(u): return u
def ease(u): return u * u * (3 - 2 * u)
def ease_in(u): return u * u
def ease_out(u): return 1 - (1 - u) ** 2
def bounce(u):
    n, d = 7.5625, 2.75
    if u < 1 / d: return n * u * u
    if u < 2 / d: u -= 1.5 / d; return n * u * u + 0.75
    if u < 2.5 / d: u -= 2.25 / d; return n * u * u + 0.9375
    u -= 2.625 / d; return n * u * u + 0.984375

EASINGS = {"linear": linear, "ease": ease, "in": ease_in, "out": ease_out, "bounce": bounce}

def get(e):
    if callable(e): return e
    if e not in EASINGS:
        raise ValueError("unknown easing %r, use one of %s" % (e, list(EASINGS)))
    return EASINGS[e]
