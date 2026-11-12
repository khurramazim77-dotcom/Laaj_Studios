"""Drawing toolkit for the Broke to Balance video: easing, AA canvas, backgrounds, icons."""
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

W, H = 1920, 1080
FPS = 30
FD = '/usr/share/fonts/opentype/inter/'

# ---- brand palette -------------------------------------------------------
NAVY = (11, 31, 58)
NAVY2 = (20, 48, 88)
INK = (16, 24, 40)
WHITE = (246, 248, 251)
GREEN = (25, 195, 125)
GREEN_D = (14, 140, 88)
GOLD = (255, 200, 61)
CORAL = (255, 107, 91)
BLUE = (47, 128, 237)
GREY = (148, 163, 184)
LIGHT = (226, 232, 240)
NEEDS, WANTS, SAVE = BLUE, GOLD, GREEN


def rgba(c, a=255):
    return (c[0], c[1], c[2], int(a))


def lerp(a, b, t):
    return a + (b - a) * t


def lerpc(c1, c2, t):
    return tuple(int(round(lerp(c1[i], c2[i], t))) for i in range(3))


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def prog(t, start, dur):
    return clamp((t - start) / dur) if dur > 0 else (1.0 if t >= start else 0.0)


def e_out(p):
    return 1 - (1 - p) ** 3


def e_inout(p):
    return 4 * p ** 3 if p < .5 else 1 - (-2 * p + 2) ** 3 / 2


def e_back(p, s=1.70158):
    p -= 1
    return 1 + (s + 1) * p ** 3 + s * p ** 2


def e_expo(p):
    return 1 if p >= 1 else 1 - 2 ** (-10 * p)


_fc = {}


def font(size, w='Bold'):
    k = (int(size), w)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(f'{FD}Inter-{w}.otf', int(size))
    return _fc[k]


def money(v, cents=False):
    return f"${v:,.2f}" if cents else f"${v:,.0f}"


class Cv:
    """Small anti-aliased layer. Draw with global coordinates; paste(img) composites it."""

    def __init__(self, bbox, s=2):
        self.x0, self.y0, x1, y1 = [int(v) for v in bbox]
        self.s = s
        self.w, self.h = max(1, x1 - self.x0), max(1, y1 - self.y0)
        self.im = Image.new('RGBA', (self.w * s, self.h * s), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)

    def P(self, x, y):
        return ((x - self.x0) * self.s, (y - self.y0) * self.s)

    def B(self, box):
        a = self.P(box[0], box[1]); b = self.P(box[2], box[3])
        return [a[0], a[1], b[0], b[1]]

    def rrect(self, box, r, fill=None, outline=None, width=1):
        self.d.rounded_rectangle(self.B(box), r * self.s, fill=fill, outline=outline, width=int(width * self.s))

    def ellipse(self, box, fill=None, outline=None, width=1):
        self.d.ellipse(self.B(box), fill=fill, outline=outline, width=int(width * self.s))

    def line(self, pts, fill, width=2, joint='curve'):
        self.d.line([self.P(*p) for p in pts], fill=fill, width=max(1, int(width * self.s)), joint=joint)

    def poly(self, pts, fill=None, outline=None):
        self.d.polygon([self.P(*p) for p in pts], fill=fill, outline=outline)

    def arc(self, box, a0, a1, fill, width):
        self.d.arc(self.B(box), a0, a1, fill=fill, width=int(width * self.s))

    def pie(self, box, a0, a1, fill):
        self.d.pieslice(self.B(box), a0, a1, fill=fill)

    def text(self, xy, s, size, w='Bold', fill=WHITE, anchor='la'):
        self.d.text(self.P(*xy), s, font=font(size * self.s, w), fill=fill, anchor=anchor)

    def paste(self, img, alpha=1.0, dx=0, dy=0):
        im = self.im
        if self.s > 1:
            im = im.resize((self.w, self.h), Image.LANCZOS)
        if alpha < 0.999:
            a = im.getchannel('A').point(lambda v: int(v * alpha))
            im = im.copy(); im.putalpha(a)
        img.paste(im, (self.x0 + int(dx), self.y0 + int(dy)), im)


def text(img, xy, s, size, w='Bold', fill=WHITE, anchor='la', alpha=1.0):
    """Direct text with optional alpha (1x)."""
    if alpha >= 0.999:
        ImageDraw.Draw(img).text(xy, s, font=font(size, w), fill=fill, anchor=anchor)
        return
    if alpha <= 0.01:
        return
    f = font(size, w)
    l, t, r, b = ImageDraw.Draw(img).textbbox(xy, s, font=f, anchor=anchor)
    pad = 6
    cv = Cv((l - pad, t - pad, r + pad, b + pad), s=1)
    cv.d.text((xy[0] - cv.x0, xy[1] - cv.y0), s, font=f, fill=fill, anchor=anchor)
    cv.paste(img, alpha)


def text_w(s, size, w='Bold'):
    return font(size, w).getlength(s)


def shadow(img, box, r=24, blur=22, a=110, off=(0, 14), color=(0, 0, 0)):
    x0, y0, x1, y1 = box
    pad = blur * 3
    cv = Cv((x0 - pad, y0 - pad, x1 + pad, y1 + pad), s=1)
    cv.rrect((x0 + off[0], y0 + off[1], x1 + off[0], y1 + off[1]), r, fill=rgba(color, a))
    cv.im = cv.im.filter(ImageFilter.GaussianBlur(blur))
    cv.paste(img)


def card(img, box, r=28, fill=WHITE, a=255, shad=True, outline=None):
    if shad:
        shadow(img, box, r)
    cv = Cv((box[0] - 3, box[1] - 3, box[2] + 3, box[3] + 3))
    cv.rrect(box, r, fill=rgba(fill, a), outline=outline, width=2)
    cv.paste(img)


def pill(img, cx, cy, s, size, bg, fg=WHITE, padx=26, h=None, w='Bold', alpha=1.0):
    tw = text_w(s, size, w)
    h = h or size * 1.9
    box = (cx - tw / 2 - padx, cy - h / 2, cx + tw / 2 + padx, cy + h / 2)
    cv = Cv((box[0] - 3, box[1] - 3, box[2] + 3, box[3] + 3))
    cv.rrect(box, h / 2, fill=rgba(bg))
    cv.paste(img, alpha)
    text(img, (cx, cy), s, size, w, fg, 'mm', alpha)


def fade_overlay(img, color, a):
    if a <= 0.003:
        return
    ov = Image.new('RGBA', img.size, rgba(color, 255 * clamp(a)))
    img.alpha_composite(ov)


# ---- backgrounds ---------------------------------------------------------
_bgc = {}


def bg_soft(img, t, c1=NAVY, c2=NAVY2, accent=GREEN, k=0):
    """Slowly drifting gradient with soft glow blobs (procedural motion background)."""
    gw, gh = 96, 54
    xs = np.linspace(0, 1, gw)[None, :]
    ys = np.linspace(0, 1, gh)[:, None]
    f = 0.5 + 0.5 * np.sin(2.2 * xs + 1.7 * ys + t * 0.18 + k)
    f = f * 0.6 + 0.4 * ys
    base = np.zeros((gh, gw, 3), np.float32)
    for i in range(3):
        base[..., i] = c1[i] + (c2[i] - c1[i]) * f
    for (bx, by, ph, col, amp) in ((0.2, 0.25, 0.0, accent, 0.20), (0.85, 0.8, 2.0, BLUE, 0.18), (0.6, 0.1, 4.0, GOLD, 0.07)):
        cx = bx + 0.10 * math.sin(t * 0.21 + ph + k)
        cy = by + 0.10 * math.cos(t * 0.17 + ph + k)
        d2 = ((xs - cx) * 1.8) ** 2 + (ys - cy) ** 2
        g = np.exp(-d2 * 9.0) * amp
        for i in range(3):
            base[..., i] += (col[i] - base[..., i]) * g
    im = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), 'RGB').resize((W, H), Image.BICUBIC)
    img.paste(im.convert('RGBA'), (0, 0))


def _skyline(seed, base_y, hmin, hmax, col, wins, span):
    rnd = random.Random(seed)
    im = Image.new('RGBA', (span, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x = -20
    while x < span:
        bw = rnd.randint(70, 190)
        bh = rnd.randint(hmin, hmax)
        d.rectangle([x, base_y - bh, x + bw, H], fill=col)
        if rnd.random() < 0.3:
            d.rectangle([x + bw * .4, base_y - bh - rnd.randint(20, 70), x + bw * .6, base_y - bh], fill=col)
        if wins:
            for wy in range(int(base_y - bh + 18), int(base_y) - 10, 28):
                for wx in range(int(x + 12), int(x + bw - 18), 24):
                    if rnd.random() < 0.28:
                        d.rectangle([wx, wy, wx + 9, wy + 14], fill=(255, 214, 120, rnd.randint(150, 240)))
        x += bw + rnd.randint(0, 14)
    return im


def bg_city(img, t):
    """Parallax dusk skyline (stands in for stock b-roll)."""
    if 'city' not in _bgc:
        sky = np.zeros((H, 1, 3), np.float32)
        top, mid, hor = np.array((10, 20, 52)), np.array((72, 52, 120)), np.array((255, 150, 96))
        for y in range(H):
            p = y / (H * 0.78)
            if p < .55:
                c = top + (mid - top) * (p / .55)
            else:
                c = mid + (hor - mid) * min(1, (p - .55) / .45)
            sky[y, 0] = c
        sky = np.repeat(sky, W, axis=1)
        s = Image.fromarray(sky.astype(np.uint8), 'RGB').convert('RGBA')
        rnd = random.Random(4)
        sd = ImageDraw.Draw(s)
        for _ in range(110):
            sd.ellipse([(x := rnd.randint(0, W)), (y := rnd.randint(0, 420)), x + 2, y + 2], fill=(255, 255, 255, rnd.randint(70, 200)))
        glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(glow).ellipse([W * .55 - 380, 760 - 380, W * .55 + 380, 760 + 380], fill=(255, 180, 110, 110))
        glow = glow.filter(ImageFilter.GaussianBlur(120))
        s.alpha_composite(glow)
        span = W * 3
        _bgc['city'] = (s,
                        _skyline(1, 860, 160, 380, (44, 38, 92, 255), False, span),
                        _skyline(2, 930, 200, 480, (26, 26, 66, 255), True, span),
                        _skyline(3, 1010, 260, 600, (12, 14, 38, 255), True, span),
                        span)
    sky, l1, l2, l3, span = _bgc['city']
    img.paste(sky, (0, 0))
    for layer, sp in ((l1, 6), (l2, 14), (l3, 26)):
        off = int(t * sp) % (span - W)
        img.paste(layer.crop((off, 0, off + W, H)), (0, 0), layer.crop((off, 0, off + W, H)))


_sprites = {}


def _coin(sz=96):
    cv = Cv((0, 0, sz, sz), s=3)
    cv.ellipse((4, 4, sz - 4, sz - 4), fill=rgba((230, 160, 20)))
    cv.ellipse((9, 9, sz - 9, sz - 9), fill=rgba(GOLD))
    cv.ellipse((17, 17, sz - 17, sz - 17), outline=rgba((230, 160, 20)), width=3)
    cv.text((sz / 2, sz / 2 + 2), '$', sz * .46, 'ExtraBold', (190, 120, 10), 'mm')
    return cv.im.resize((sz, sz), Image.LANCZOS)


def _bill(w=170, h=84):
    cv = Cv((0, 0, w, h), s=3)
    cv.rrect((2, 2, w - 2, h - 2), 10, fill=rgba((52, 170, 110)))
    cv.rrect((9, 9, w - 9, h - 9), 6, outline=rgba((190, 240, 210), 200), width=2)
    cv.ellipse((w / 2 - 22, h / 2 - 22, w / 2 + 22, h / 2 + 22), fill=rgba((190, 240, 210)))
    cv.text((w / 2, h / 2 + 1), '$', 30, 'ExtraBold', (36, 120, 80), 'mm')
    return cv.im.resize((w, h), Image.LANCZOS)


def money_rain(img, t, n=18, seed=7, alpha=0.9, up=False):
    if 'coin' not in _sprites:
        _sprites['coin'] = _coin(); _sprites['bill'] = _bill()
        _sprites['coin_b'] = _sprites['coin'].filter(ImageFilter.GaussianBlur(3))
        _sprites['bill_b'] = _sprites['bill'].filter(ImageFilter.GaussianBlur(3))
    rnd = random.Random(seed)
    items = []
    for i in range(n):
        kind = 'coin' if rnd.random() < .55 else 'bill'
        depth = rnd.random()
        items.append((kind, rnd.random() * W, rnd.random() * (H + 300), 60 + 140 * (1 - depth) * (0.6 + rnd.random() * .5), rnd.random() * 360, (rnd.random() - .5) * 120, 0.35 + 0.75 * (1 - depth), depth, rnd.random() * 6))
    items.sort(key=lambda it: -it[7])
    for kind, x, y0, v, a0, av, sc, depth, ph in items:
        y = (y0 + v * t) % (H + 300) - 150
        xx = x + 40 * math.sin(t * .8 + ph)
        sp = _sprites[kind + ('_b' if depth > .75 else '')]
        sp2 = sp.resize((int(sp.width * sc), int(sp.height * sc)), Image.BILINEAR)
        if kind == 'coin':
            squash = abs(math.cos(math.radians(a0 + av * t)))
            sp2 = sp2.resize((max(4, int(sp2.width * (0.25 + 0.75 * squash))), sp2.height), Image.BILINEAR)
        else:
            sp2 = sp2.rotate(a0 + av * t * .5, resample=Image.BICUBIC, expand=True)
        al = alpha * (0.45 + 0.55 * (1 - depth))
        if al < 0.99:
            sp2 = sp2.copy(); sp2.putalpha(sp2.getchannel('A').point(lambda v_: int(v_ * al)))
        img.paste(sp2, (int(xx - sp2.width / 2), int(y - sp2.height / 2)), sp2)


# ---- icons ---------------------------------------------------------------
def icon(img, kind, cx, cy, r=34, col=WHITE, bg=None, alpha=1.0):
    cv = Cv((cx - r - 4, cy - r - 4, cx + r + 4, cy + r + 4), s=3)
    if bg is not None:
        cv.ellipse((cx - r, cy - r, cx + r, cy + r), fill=rgba(bg))
    u = r / 34.0
    X = lambda dx: cx + dx * u
    Y = lambda dy: cy + dy * u
    c = rgba(col)
    if kind == 'house':
        cv.poly([(X(-16), Y(-2)), (X(0), Y(-16)), (X(16), Y(-2))], fill=c)
        cv.rrect((X(-11), Y(-2), X(11), Y(14)), 2, fill=c)
        cv.rrect((X(-3), Y(5), X(3), Y(14)), 1, fill=rgba(bg or NAVY))
    elif kind == 'cart':
        cv.line([(X(-16), Y(-12)), (X(-10), Y(-12)), (X(-6), Y(6)), (X(11), Y(6))], c, 3.5 * u)
        cv.poly([(X(-9), Y(-7)), (X(14), Y(-7)), (X(11), Y(3)), (X(-6), Y(3))], fill=c)
        cv.ellipse((X(-8), Y(9), X(-3), Y(14)), fill=c); cv.ellipse((X(6), Y(9), X(11), Y(14)), fill=c)
    elif kind == 'bolt':
        cv.poly([(X(3), Y(-17)), (X(-9), Y(3)), (X(-1), Y(3)), (X(-4), Y(17)), (X(10), Y(-4)), (X(2), Y(-4))], fill=c)
    elif kind == 'car':
        cv.rrect((X(-17), Y(-2), X(17), Y(10)), 4, fill=c)
        cv.poly([(X(-10), Y(-2)), (X(-6), Y(-11)), (X(7), Y(-11)), (X(12), Y(-2))], fill=c)
        for dx in (-9, 9):
            cv.ellipse((X(dx - 4.5), Y(7), X(dx + 4.5), Y(16)), fill=c, outline=rgba(bg or NAVY), width=2 * u)
    elif kind == 'shield':
        cv.poly([(X(0), Y(-17)), (X(15), Y(-11)), (X(14), Y(3)), (X(0), Y(17)), (X(-14), Y(3)), (X(-15), Y(-11))], fill=c)
        cv.line([(X(-6), Y(0)), (X(-1), Y(5)), (X(7), Y(-5))], rgba(bg or NAVY), 3.5 * u)
    elif kind == 'fork':
        cv.ellipse((X(-4), Y(-14), X(16), Y(6)), outline=c, width=3 * u)
        cv.line([(X(-11), Y(-14)), (X(-11), Y(14))], c, 3 * u)
        cv.line([(X(-15), Y(-14)), (X(-15), Y(-4)), (X(-7), Y(-4)), (X(-7), Y(-14))], c, 2.5 * u)
        cv.line([(X(6), Y(8)), (X(6), Y(15))], c, 3 * u)
    elif kind == 'play':
        cv.rrect((X(-16), Y(-11), X(16), Y(11)), 5, outline=c, width=3 * u)
        cv.poly([(X(-4), Y(-5)), (X(-4), Y(5)), (X(6), Y(0))], fill=c)
    elif kind == 'bag':
        cv.rrect((X(-13), Y(-5), X(13), Y(15)), 4, fill=c)
        cv.arc((X(-7), Y(-15), X(7), Y(1)), 180, 360, c, 3 * u)
    elif kind == 'star':
        pts = []
        for i in range(10):
            ang = -math.pi / 2 + i * math.pi / 5
            rr = 17 if i % 2 == 0 else 7.5
            pts.append((X(rr * math.cos(ang)), Y(rr * math.sin(ang))))
        cv.poly(pts, fill=c)
    elif kind == 'plane':
        cv.poly([(X(-16), Y(2)), (X(16), Y(-12)), (X(6), Y(14)), (X(1), Y(5))], fill=c)
    elif kind == 'dots':
        for dx in (-10, 0, 10):
            cv.ellipse((X(dx - 3.4), Y(-3.4), X(dx + 3.4), Y(3.4)), fill=c)
    elif kind == 'piggy':   # coin glyph
        cv.ellipse((X(-15), Y(-15), X(15), Y(15)), outline=c, width=3.5 * u)
        cv.text((cx, cy + 1 * u), '$', int(24 * u), 'ExtraBold', c, 'mm')
    elif kind == 'x':
        cv.line([(X(-11), Y(-11)), (X(11), Y(11))], c, 5 * u)
        cv.line([(X(11), Y(-11)), (X(-11), Y(11))], c, 5 * u)
    elif kind == 'check':
        cv.line([(X(-12), Y(1)), (X(-4), Y(9)), (X(13), Y(-9))], c, 5 * u)
    cv.paste(img, alpha)


def logo_chip(img, a=1.0):
    cv = Cv((36, 28, 420, 108))
    cv.rrect((40, 32, 416, 104), 36, fill=rgba(NAVY, 190), outline=rgba(WHITE, 40), width=2)
    cv.ellipse((54, 46, 98, 90), fill=rgba(GREEN))
    cv.line([(62, 60), (90, 60)], rgba(WHITE), 3.5)
    cv.poly([(76, 60), (70, 78), (82, 78)], fill=rgba(WHITE))
    cv.line([(66, 64), (62, 74), (70, 74), (66, 64)], rgba(WHITE), 1.5)
    cv.line([(86, 64), (82, 74), (90, 74), (86, 64)], rgba(WHITE), 1.5)
    cv.paste(img, a)
    text(img, (112, 68), 'Broke', 25, 'ExtraBold', CORAL, 'lm', a)
    x = 112 + text_w('Broke', 25, 'ExtraBold') + 10
    text(img, (x, 68), '→', 25, 'Bold', GREY, 'lm', a)
    text(img, (x + 30, 68), 'Balance', 25, 'ExtraBold', GREEN, 'lm', a)


def count_text(v, cents=False):
    return money(v, cents)
