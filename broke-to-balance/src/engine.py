"""Episode engine: a spec (script + visual elements) -> scene renderers + sound events.
Each episode picks a STYLE (theme / background / header / transitions / music) while the brand
constants (logo chip, Inter, palette, sting, end card) stay the same across the channel."""
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import lib as _lib
from lib import *

TH = {}
CONTENT = (140, 300, 1780, 940)


# ---------------------------------------------------------------- themes / backgrounds
THEMES = {
    'night': dict(paper=False, txt=WHITE, sub=GREY, grid=(255, 255, 255, 34), panel=(255, 255, 255, 26), edge=170, ink=NAVY),
    'paper': dict(paper=True, txt=(18, 36, 66), sub=(104, 116, 140), grid=(18, 36, 66, 30), panel=(255, 255, 255, 255), edge=255, ink=(18, 36, 66)),
}
_tile = {}


def _grid_tile(kind):
    if kind in _tile:
        return _tile[kind]
    t = Image.new('RGBA', (96, 96), (0, 0, 0, 0)); d = ImageDraw.Draw(t)
    if kind == 'dots':
        d.ellipse([46, 46, 50, 50], fill=(255, 255, 255, 40))
    elif kind == 'hud':
        d.line([(0, 0), (96, 0)], fill=(120, 190, 255, 38), width=1); d.line([(0, 0), (0, 96)], fill=(120, 190, 255, 38), width=1)
        d.rectangle([0, 0, 3, 3], fill=(120, 190, 255, 90))
    elif kind == 'stripes':
        for i in range(-96, 192, 24):
            d.line([(i, 96), (i + 96, 0)], fill=(255, 255, 255, 14), width=6)
    _tile[kind] = t
    return t


def _tiled(img, kind, ox=0, oy=0):
    t = _grid_tile(kind)
    big = Image.new('RGBA', (W + 96, H + 96), (0, 0, 0, 0))
    for x in range(0, W + 96, 96):
        for y in range(0, H + 96, 96):
            big.paste(t, (x, y))
    ox, oy = int(ox) % 96, int(oy) % 96
    img.alpha_composite(big.crop((ox, oy, ox + W, oy + H)))


def background(img, t, bg):
    k = bg.get('kind', 'soft'); tt = t
    if k == 'city':
        _lib.bg_city(img, tt); fade_overlay(img, (8, 14, 36), 0.28)
    elif k == 'rain':
        _lib.bg_soft(img, tt, NAVY, NAVY2, bg.get('accent', GREEN), bg.get('k', 1)); _lib.money_rain(img, tt + 5, 22, 11, 0.85); fade_overlay(img, NAVY, 0.25)
    elif k == 'dots':       # investigation board / graph paper
        _lib.bg_soft(img, tt, (14, 20, 36), (34, 28, 52), bg.get('accent', CORAL), bg.get('k', 2)); _tiled(img, 'dots', tt * 12, tt * 6)
    elif k == 'hud':        # game-HUD grid
        _lib.bg_soft(img, tt, (8, 12, 40), (24, 22, 84), bg.get('accent', (90, 140, 255)), bg.get('k', 3)); _tiled(img, 'hud', tt * 10, tt * 10)
    elif k == 'versus':     # two-corner showdown glow
        _lib.bg_soft(img, tt, (10, 16, 40), (30, 20, 56), BLUE, bg.get('k', 4))
        glow = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(glow)
        d.ellipse([-500, 100, 900, 1300], fill=(47, 128, 237, 90)); d.ellipse([1020, 100, 2420, 1300], fill=(255, 107, 91, 80))
        img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(160))); _tiled(img, 'stripes', tt * 14, 0)
    elif k == 'paper':      # planner paper
        img.paste(Image.new('RGBA', (W, H), (250, 246, 236, 255)), (0, 0))
        d = ImageDraw.Draw(img, 'RGBA')
        for y in range(190, H, 54):
            d.line([(0, y), (W, y)], fill=(120, 150, 200, 55), width=2)
        d.line([(150, 0), (150, H)], fill=(255, 107, 91, 90), width=3)
        g = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse([1200, -300, 2300, 500], fill=(255, 200, 61, 60))
        img.alpha_composite(g.filter(ImageFilter.GaussianBlur(120)))
    else:
        _lib.bg_soft(img, tt, bg.get('c1', NAVY), bg.get('c2', NAVY2), bg.get('accent', GREEN), bg.get('k', 0))


# ---------------------------------------------------------------- refs, helpers
def parse_ref(ref, S):
    if isinstance(ref, (int, float)):
        return float(ref)
    if '+' in ref:
        k, o = ref.split('+'); return S[k][0] + float(o)
    return S[ref][0]


def dprog(t, start, dur):      # real-time duration (independent of animation speed)
    return prog(t, start, dur * _lib.SPEED)


def fmtv(v, f='money'):
    if f == 'money':
        return money(v)
    if f == 'pct':
        return f'{v:.0f}%'
    if f == 'int':
        return f'{v:,.0f}'
    if f == 'mo':
        return f'{v:.0f} mo'
    return str(v)


def wrap(s, size, maxw, w='Medium'):
    out, cur = [], ''
    for wd in s.split():
        t = (cur + ' ' + wd).strip()
        if text_w(t, size, w) <= maxw or not cur:
            cur = t
        else:
            out.append(cur); cur = wd
    out.append(cur)
    return out


def panel(img, box, col, al=1.0, r=28, fillcol=None):
    x0, y0, x1, y1 = box
    if TH['paper']:
        shadow(img, box, r, 18, int(70 * al), (0, 10))
        cv = Cv((x0 - 3, y0 - 3, x1 + 3, y1 + 3)); cv.rrect(box, r, fill=rgba(fillcol or (255, 255, 255)), outline=rgba(col, 230), width=3); cv.paste(img, al)
    else:
        cv = Cv((x0 - 3, y0 - 3, x1 + 3, y1 + 3)); cv.rrect(box, r, fill=TH['panel'] if fillcol is None else rgba(fillcol, 255), outline=rgba(col, TH['edge']), width=2); cv.paste(img, al)


def txt(img, xy, s, size, w='Bold', col=None, anchor='mm', al=1.0):
    text(img, xy, s, size, w, col or TH['txt'], anchor, al)


def sub(img, xy, s, size, w='Medium', anchor='mm', al=1.0):
    text(img, xy, s, size, w, TH['sub'], anchor, al)


# ---------------------------------------------------------------- headers (one per style)
def draw_header(img, t, h, a0):
    if not h:
        return
    style, tag, title, col = h['style'], h['tag'], h['title'], h.get('color', GREEN)
    p = e_out(prog(t, a0, 0.5))
    if p <= 0:
        return
    if style == 'pill':
        pill(img, 960, 168 - 20 * (1 - p), tag, 24, col, NAVY if col in (GOLD, GREEN) else WHITE, padx=24, h=44, alpha=p)
        txt(img, (960, 232 - 20 * (1 - p)), title, 58, 'ExtraBold', None, 'mm', p)
    elif style == 'stamp':   # investigation case-file label, left aligned
        cv = Cv((130, 120, 700, 230), s=2); cv.rrect((150, 140, 150 + text_w(tag, 28, 'Black') + 56, 196), 8, outline=rgba(col, 255), width=4); cv.paste(img, p, dx=0, dy=0)
        text(img, (178, 168), tag, 28, 'Black', col, 'lm', p)
        txt(img, (150 - 40 * (1 - p), 252), title, 62, 'Black', None, 'lm', p)
        cvl = Cv((140, 280, 1100, 296)); cvl.rrect((150, 284, 150 + 520 * p, 292), 4, fill=rgba(col)); cvl.paste(img)
    elif style == 'band':    # top band with title left, tag right
        ImageDraw.Draw(img, 'RGBA').rectangle([0, 132, W, 232], fill=rgba(NAVY, int(150 * p)))
        text(img, (150, 182), title, 56, 'Black', WHITE, 'lm', p)
        pill(img, W - 260, 182, tag, 26, col, WHITE, padx=26, h=52, alpha=p)
    elif style == 'hud':     # LEVEL chip + segmented bar
        pill(img, 250, 176, tag, 26, col, NAVY, padx=26, h=50, alpha=p)
        txt(img, (150, 250), title, 60, 'ExtraBold', None, 'lm', p)
        for i in range(h.get('segs', 5)):
            c = col if i < h.get('on', 1) else (60, 70, 120)
            cv = Cv((430 + i * 52, 160, 482 + i * 52, 192)); cv.rrect((434 + i * 52, 168, 474 + i * 52, 184), 6, fill=rgba(c)); cv.paste(img, p)
    elif style == 'tab':     # planner tab on paper
        cv = Cv((140, 120, 760, 210)); cv.rrect((150, 130, 150 + text_w(tag, 26, 'Black') + 60, 196), 16, fill=rgba(col)); cv.paste(img, p)
        text(img, (180, 163), tag, 26, 'Black', NAVY, 'lm', p)
        txt(img, (150 - 30 * (1 - p), 252), title, 60, 'Black', None, 'lm', p)


# ---------------------------------------------------------------- elements
def el_title(img, t, S, el, R):
    x0, y0, x1, y1 = el.get('region', CONTENT); a0 = R(el['at']); lines = el['lines']
    tot = sum(l[1] * 1.28 for l in lines); y = (y0 + y1) / 2 - tot / 2
    for i, (s, size, col, w) in enumerate(lines):
        p = e_out(prog(t, a0 + 0.18 * i, .5))
        text(img, ((x0 + x1) / 2, y + size * .64 + 24 * (1 - p)), s, size, w, col or TH['txt'], 'mm', p)
        y += size * 1.28


def el_bullets(img, t, S, el, R):
    x0, y0, x1, y1 = el.get('region', CONTENT); items = el['items']; n = len(items)
    rh = min(el.get('rowh', 128), (y1 - y0) / n); size = el.get('size', 40)
    for i, it in enumerate(items):
        p = e_back(prog(t, R(it['at']), .5)); al = clamp(p)
        if al <= 0:
            continue
        y = y0 + rh * (i + .5); x = x0 + 70 * (1 - al); col = it.get('color', GREEN)
        panel(img, (x, y - rh / 2 + 8, x1, y + rh / 2 - 8), col, al, 26)
        if it.get('icon'):
            icon(img, it['icon'], x + 66, y, 34, NAVY, col, al)
        else:
            cv = Cv((x + 26, y - 40, x + 106, y + 40)); cv.ellipse((x + 30, y - 36, x + 102, y + 36), fill=rgba(col)); cv.paste(img, al)
            text(img, (x + 66, y), str(i + 1), 40, 'Black', NAVY, 'mm', al)
        if it.get('sub'):
            txt(img, (x + 134, y - 20), it['text'], size, 'Bold', None, 'lm', al); sub(img, (x + 134, y + 28), it['sub'], int(size * .66), 'Medium', 'lm', al)
        else:
            txt(img, (x + 134, y), it['text'], size, 'Bold', None, 'lm', al)


def el_bars(img, t, S, el, R):
    x0, y0, x1, y1 = el.get('region', CONTENT); items = el['items']; n = len(items)
    rh = min(108, (y1 - y0) / n); mx = el.get('max') or max(i['value'] for i in items); lw = el.get('labelw', 400); f = el.get('fmt', 'money')
    bx0, bx1 = x0 + lw + 60, x1 - 230
    for i, it in enumerate(items):
        p = e_out(dprog(t, R(it['at']), .7)); al = clamp(p * 3)
        if al <= 0:
            continue
        y = y0 + rh * (i + .5); col = it.get('color', GOLD)
        if it.get('icon'):
            icon(img, it['icon'], x0 + 38, y, 34, NAVY, col, al)
        txt(img, (x0 + 100, y), it['label'], el.get('size', 34), 'SemiBold', None, 'lm', al)
        cv = Cv((bx0 - 3, y - 30, bx1 + 230, y + 30))
        cv.rrect((bx0, y - 22, bx1, y + 22), 22, fill=rgba(TH['txt'], 26))
        cv.rrect((bx0, y - 22, bx0 + max(44, (bx1 - bx0) * it['value'] / mx * p), y + 22), 22, fill=rgba(col)); cv.paste(img)
        text(img, (bx1 + 28, y), it.get('display') or fmtv(it['value'] * p, f), 34, 'Black', col if not TH['paper'] else TH['txt'], 'lm', al)


def el_columns(img, t, S, el, R):
    x0, y0, x1, y1 = el.get('region', CONTENT); items = el['items']; n = len(items); f = el.get('fmt', 'money')
    base = y1 - 90; mx = el.get('max') or max(i['value'] for i in items); bw = min(220, (x1 - x0) / n * .6); gap = (x1 - x0) / n
    ImageDraw.Draw(img, 'RGBA').line([(x0, base), (x1, base)], fill=TH['grid'][:3] + (160,), width=3)
    for i, it in enumerate(items):
        p = e_out(dprog(t, R(it['at']), .8))
        if p <= 0:
            continue
        cx = x0 + gap * (i + .5); h = (base - y0 - 70) * it['value'] / mx * p; col = it.get('color', GREEN)
        cv = Cv((cx - bw / 2 - 4, base - h - 4, cx + bw / 2 + 4, base + 4)); cv.rrect((cx - bw / 2, base - h, cx + bw / 2, base), 18, fill=rgba(col)); cv.paste(img)
        text(img, (cx, base - h - 40), it.get('display') or fmtv(it['value'], f), 48, 'Black', col if not TH['paper'] else TH['txt'], 'mm', clamp(p * 2))
        txt(img, (cx, base + 40), it['label'], 30, 'Bold', None, 'mm', clamp(p * 2))
        if it.get('sub'):
            sub(img, (cx, base + 76), it['sub'], 24, 'Medium', 'mm', clamp(p * 2))


def el_donut(img, t, S, el, R):
    x0, y0, x1, y1 = el.get('region', CONTENT); items = el['items']
    leg = el.get('legend', True); cx = x0 + (x1 - x0) * (.28 if leg else .5); cy = (y0 + y1) / 2; Rr = min(x1 - x0, y1 - y0) * (.46 if leg else .44); r = Rr * .62
    cv = Cv((cx - Rr - 10, cy - Rr - 10, cx + Rr + 10, cy + Rr + 10), s=3)
    cv.ellipse((cx - Rr, cy - Rr, cx + Rr, cy + Rr), fill=rgba(TH['txt'], 22))
    a = -90.0
    for it in items:
        sweep = 360 * it['frac']; p = e_inout(dprog(t, R(it['at']), .9))
        if p > .003:
            cv.pie((cx - Rr, cy - Rr, cx + Rr, cy + Rr), a + .8, max(a + 1, a + sweep * p - .8), rgba(it['color']))
        a += sweep
    cv.d.ellipse(cv.B((cx - r, cy - r, cx + r, cy + r)), fill=(0, 0, 0, 0))
    cv.ellipse((cx - r, cy - r, cx + r, cy + r), fill=rgba((255, 255, 255) if TH['paper'] else NAVY)); cv.paste(img)
    c = el.get('center')
    if c:
        txt(img, (cx, cy - 8), c[0], c[1], 'Black', None, 'mm'); sub(img, (cx, cy + c[1] * .55), c[2] if len(c) > 2 else '', 26)
    if leg:
        n = len(items)
        for i, it in enumerate(items):
            p = e_out(prog(t, R(it['at']) + .1, .5)); y = cy + (i - (n - 1) / 2) * 120; x = x0 + (x1 - x0) * .58
            if p <= 0:
                continue
            panel(img, (x + 40 * (1 - p), y - 48, x1 + 40 * (1 - p), y + 48), it['color'], p, 24)
            txt(img, (x + 40 * (1 - p) + 36, y), it['label'], 34, 'Bold', None, 'lm', p)
            text(img, (x1 - 30 + 40 * (1 - p), y), it.get('display', f"{it['frac'] * 100:.0f}%"), 42, 'Black', it['color'] if not TH['paper'] else TH['txt'], 'rm', p)


def el_line(img, t, S, el, R):
    x0, y0, x1, y1 = el.get('region', CONTENT); a0 = R(el['at']); dur = el.get('dur', 3)
    px0, px1, py0, py1 = x0 + 150, x1 - el.get('rightpad', 330), y0 + 30, y1 - 70
    ymax = el['ymax']; step = el.get('ystep', ymax / 4); N = len(el['series'][0]['values']) - 1
    X = lambda i: px0 + (px1 - px0) * i / N; Y = lambda v: py1 - (py1 - py0) * v / ymax
    d = ImageDraw.Draw(img, 'RGBA'); v = 0
    while v <= ymax + 1e-6:
        d.line([(px0, Y(v)), (px1, Y(v))], fill=TH['grid'], width=1); sub(img, (px0 - 20, Y(v)), fmtv(v, el.get('fmt', 'money')), 24, 'Medium', 'rm'); v += step
    for i, lab in el.get('xlabels', []):
        sub(img, (X(i), py1 + 34), lab, 24)
    p = e_inout(dprog(t, a0, dur))
    cv = Cv((px0 - 12, y0 - 20, x1 + 20, py1 + 20), s=2)
    for s in el['series']:
        m = N * p; vals = s['values']
        pts = [(X(i), Y(vals[i])) for i in range(int(m) + 1)]
        if m > int(m) and int(m) < N:
            f = m - int(m); pts.append((X(m), Y(lerp(vals[int(m)], vals[int(m) + 1], f))))
        if len(pts) > 1:
            cv.line(pts, rgba(s['color']), s.get('width', 8))
        if pts:
            cv.ellipse((pts[-1][0] - 12, pts[-1][1] - 12, pts[-1][0] + 12, pts[-1][1] + 12), fill=rgba(WHITE), outline=rgba(s['color']), width=5)
    cv.paste(img)
    for mk in el.get('markers', []):
        q = e_back(dprog(t, R(mk['at']), .5))
        if q > 0:
            s_ = el['series'][mk.get('series', 0)]; xi = mk['x']
            pill(img, X(xi) + mk.get('dx', 60), Y(s_['values'][xi]) + mk.get('dy', -64), mk['label'], 28, mk.get('color', s_['color']), NAVY, padx=24, h=56, alpha=clamp(q))
    if p >= .999:
        for s in el['series']:
            if s.get('endlabel'):
                text(img, (px1 + 28, Y(s['values'][-1]) - (18 if s.get('endsub') else 0)), s['endlabel'], 44, 'Black', s['color'], 'lm')
                if s.get('endsub'):
                    sub(img, (px1 + 28, Y(s['values'][-1]) + 26), s['endsub'], 24, 'Medium', 'lm')


def el_table(img, t, S, el, R):
    x0, y0, x1, y1 = el.get('region', (130, 300, 1170, 960)); cols = el['cols']; rows = el['rows']; rh = el.get('rowh', 56)
    ft = el.get('formula', ('A1', ''))
    box = (x0, y0, x1, y1)
    shadow(img, box, 22, 30, 120); cv = Cv((x0 - 3, y0 - 3, x1 + 3, y1 + 3)); cv.rrect(box, 22, fill=rgba((252, 253, 255)))
    cv.rrect((x0, y0, x1, y0 + 58), 22, fill=rgba((232, 238, 246))); cv.rrect((x0, y0 + 30, x1, y0 + 58), 0, fill=rgba((232, 238, 246)))
    for i, c in enumerate(((255, 95, 87), (254, 188, 46), (40, 200, 64))):
        cv.ellipse((x0 + 24 + i * 30, y0 + 20, x0 + 40 + i * 30, y0 + 36), fill=rgba(c))
    cv.paste(img)
    text(img, ((x0 + x1) / 2, y0 + 29), el.get('title', 'Budget.xlsx'), 24, 'SemiBold', (80, 92, 112), 'mm')
    d = ImageDraw.Draw(img); fy = y0 + 58
    d.rectangle([x0, fy, x1, fy + 52], fill=(245, 247, 251)); d.rectangle([x0 + 12, fy + 8, x0 + 112, fy + 44], fill=WHITE, outline=(200, 208, 220))
    text(img, (x0 + 62, fy + 26), ft[0], 24, 'SemiBold', (60, 70, 90), 'mm'); text(img, (x0 + 140, fy + 26), 'fx', 24, 'Bold', (120, 130, 150), 'mm'); text(img, (x0 + 175, fy + 26), ft[1], 26, 'Medium', (30, 40, 60), 'lm')
    ry = fy + 52
    tw = sum(c[1] for c in cols); xs = [x0]
    for c in cols:
        xs.append(xs[-1] + c[1] * (x1 - x0) / tw)
    d.rectangle([x0, ry, x1, ry + rh], fill=(226, 236, 252))
    for i, c in enumerate(cols):
        xx = xs[i] + 16 if i == 0 else xs[i + 1] - 16
        text(img, (xx, ry + rh / 2), c[0], 26, 'Bold', (30, 60, 130), 'lm' if i == 0 else 'rm')
    nrows = int((y1 - ry - rh) // rh)
    for rr in range(nrows + 1):
        yy = ry + rh * (rr + 1); d.line([(x0, yy), (x1, yy)], fill=(226, 231, 240), width=1)
    for i in range(1, len(cols)):
        d.line([(xs[i], ry), (xs[i], ry + rh * (nrows + 1))], fill=(226, 231, 240), width=1)
    for i, row in enumerate(rows):
        p = e_out(prog(t, R(row['at']), .45))
        if p <= 0:
            continue
        yy = ry + rh * (i + 1); st = row.get('style')
        if st == 'total':
            dd = ImageDraw.Draw(img, 'RGBA'); dd.rectangle([x0 + 1, yy + 1, x1 - 1, yy + rh - 1], fill=rgba(GREEN, 60 * p))
        if st == 'bad':
            dd = ImageDraw.Draw(img, 'RGBA'); dd.rectangle([x0 + 1, yy + 1, x1 - 1, yy + rh - 1], fill=rgba(CORAL, 70 * p))
        for j, cell in enumerate(row['cells']):
            xx = xs[j] + 16 if j == 0 else xs[j + 1] - 16
            colr = (10, 90, 60) if st == 'total' else ((150, 30, 20) if st == 'bad' else (30, 40, 60))
            text(img, (xx, yy + rh / 2), cell, 27, 'ExtraBold' if st else 'Medium', colr, 'lm' if j == 0 else 'rm', p)


def el_counter(img, t, S, el, R):
    x0, y0, x1, y1 = el.get('region', CONTENT); a0 = R(el['at']); f = el.get('fmt', 'money'); size = el.get('size', 150)
    p = e_out(dprog(t, a0, el.get('dur', 1.4))) if el.get('dur', 1.4) > 0 else 1
    v = lerp(el.get('from', 0), el.get('to', 0), p); cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    if el.get('label'):
        sub(img, (cx, cy - size * .75), el['label'], 32, 'Bold')
    col = el.get('color', GREEN)
    text(img, (cx, cy), el.get('text') or fmtv(v, f), size, 'Black', col if not TH['paper'] else TH['txt'], 'mm', clamp(p * 4 + .2))
    if el.get('note'):
        sub(img, (cx, cy + size * .72), el['note'], 32, 'Medium')


def el_gauge(img, t, S, el, R):
    x0, y0, x1, y1 = el.get('region', CONTENT); a0 = R(el['at']); cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; Rr = min(x1 - x0, y1 - y0) * .42
    full = el.get('full', True); p = e_inout(dprog(t, a0, el.get('dur', 1.6))); frac = el['frac'] * p; col = el.get('color', GREEN)
    cv = Cv((cx - Rr - 40, cy - Rr - 40, cx + Rr + 40, cy + Rr + 40), s=3)
    if full:
        cv.arc((cx - Rr, cy - Rr, cx + Rr, cy + Rr), 0, 360, rgba(TH['txt'], 34), 46)
        cv.arc((cx - Rr, cy - Rr, cx + Rr, cy + Rr), -90, -90 + 360 * frac, rgba(col), 46)
    else:
        cv.arc((cx - Rr, cy - Rr, cx + Rr, cy + Rr), 180, 360, rgba(TH['txt'], 34), 46)
        for z in el.get('zones', []):
            cv.arc((cx - Rr, cy - Rr, cx + Rr, cy + Rr), 180 + 180 * z[0], 180 + 180 * z[1] - .6, rgba(z[2]), 46)
        a = math.radians(180 + 180 * frac); nx, ny = cx + (Rr - 70) * math.cos(a), cy + (Rr - 70) * math.sin(a)
        cv.line([(cx, cy), (nx, ny)], rgba(TH['txt']), 10); cv.ellipse((cx - 18, cy - 18, cx + 18, cy + 18), fill=rgba(TH['txt']))
    cv.paste(img)
    if el.get('valtext'):
        vt = el['valtext']; shown = vt(frac / max(el['frac'], 1e-6) if el['frac'] else 0) if callable(vt) else vt
        txt(img, (cx, cy + (0 if full else -Rr * .28)), shown, el.get('size', 120), 'Black', None, 'mm')
    if el.get('label'):
        sub(img, (cx, cy + (Rr * .42 if full else 54)), el['label'], 30)


def el_cards(img, t, S, el, R):
    x0, y0, x1, y1 = el.get('region', CONTENT); items = el['items']; n = len(items); gap = 34; w = (x1 - x0 - gap * (n - 1)) / n
    for i, it in enumerate(items):
        p = e_back(prog(t, R(it['at']), .6)); al = clamp(p)
        if al <= 0:
            continue
        x = x0 + i * (w + gap); yo = 50 * (1 - al); col = it.get('color', GREEN); box = (x, y0 + yo, x + w, y1 + yo)
        panel(img, box, col, al, 32)
        if it.get('icon'):
            icon(img, it['icon'], x + 78, y0 + yo + 84, 44, NAVY, col, al)
        if it.get('big'):
            text(img, (x + w - 40, y0 + yo + 84), it['big'], 70, 'Black', col if not TH['paper'] else TH['txt'], 'rm', al)
        txt(img, (x + 36, y0 + yo + 190), it['title'], it.get('tsize', 36), 'ExtraBold', None, 'lm', al)
        yy = y0 + yo + 250
        for ln in it.get('body', []):
            for l2 in wrap(ln, 28, w - 72):
                sub(img, (x + 36, yy), l2, 28, 'Medium', 'lm', al); yy += 40
            yy += 8


def el_compare(img, t, S, el, R):
    x0, y0, x1, y1 = el.get('region', CONTENT); gap = 50; w = (x1 - x0 - gap) / 2
    for k, side in enumerate(('left', 'right')):
        sd = el[side]; x = x0 + k * (w + gap); p = e_out(prog(t, R(sd['at']), .6))
        if p <= 0:
            continue
        col = sd['color']; xo = (-1 if k == 0 else 1) * 60 * (1 - p)
        panel(img, (x + xo, y0, x + w + xo, y1), col, p, 32)
        if sd.get('icon'):
            icon(img, sd['icon'], x + xo + 70, y0 + 66, 36, NAVY, col, p)
        txt(img, (x + xo + (130 if sd.get('icon') else 40), y0 + 66), sd['title'], 42, 'Black', col if not TH['paper'] else TH['txt'], 'lm', p)
        ImageDraw.Draw(img, 'RGBA').line([(x + xo + 30, y0 + 124), (x + xo + w - 30, y0 + 124)], fill=rgba(col, 120 * p), width=3)
        for i, ln in enumerate(sd['lines']):
            ts = R(ln['at']) if isinstance(ln, dict) else R(sd['at']) + .5 + i * .45
            s = ln['text'] if isinstance(ln, dict) else ln; q = e_out(prog(t, ts, .4))
            if q > 0:
                yy = y0 + 190 + i * sd.get('step', 92)
                icon(img, sd.get('bullet', 'check' if k == 0 else 'x'), x + xo + 56, yy, 22, col, None, q)
                txt(img, (x + xo + 100, yy), s, sd.get('size', 32), 'SemiBold', None, 'lm', q)


def el_calendar(img, t, S, el, R):
    x0, y0, x1, y1 = el.get('region', (140, 290, 1180, 960)); a0 = R(el['at']); days = el.get('days', 28); start = el.get('start', 0)
    panel(img, (x0, y0, x1, y1), el.get('color', BLUE), clamp(prog(t, a0, .5)), 30)
    txt(img, (x0 + 40, y0 + 46), el.get('title', 'Month'), 40, 'Black', None, 'lm', clamp(prog(t, a0, .5)))
    cw = (x1 - x0 - 60) / 7; weeks = (start + days + 6) // 7; ch = min(110, (y1 - y0 - 150) / weeks)
    for i, dn in enumerate('SMTWTFS'):
        sub(img, (x0 + 30 + cw * (i + .5), y0 + 110), dn, 24, 'Bold')
    marks = {m['day']: m for m in el.get('marks', [])}
    for dd in range(1, days + 1):
        idx = start + dd - 1; cx = x0 + 30 + cw * (idx % 7 + .5); cy = y0 + 160 + ch * (idx // 7 + .5)
        m = marks.get(dd); p = e_back(prog(t, R(m['at']), .45)) if m else 0
        if m and p > 0:
            cv = Cv((cx - 44, cy - 44, cx + 44, cy + 44)); cv.ellipse((cx - 38 * clamp(p), cy - 38 * clamp(p), cx + 38 * clamp(p), cy + 38 * clamp(p)), fill=rgba(m['color'])); cv.paste(img)
            text(img, (cx, cy), str(dd), 28, 'Black', NAVY, 'mm')
            if m.get('label'):
                text(img, (cx, cy + 38), m['label'], 18, 'Bold', m['color'] if not TH['paper'] else TH['txt'], 'mm', clamp(p))
        else:
            sub(img, (cx, cy), str(dd), 26, 'Medium')


def el_race(img, t, S, el, R):
    x0, y0, x1, y1 = el.get('region', CONTENT); a0 = R(el['at']); dur = el.get('dur', 10); ser = el['series']; n = len(ser)
    N = max(len(s['balances']) for s in ser) - 1; p = clamp(dprog(t, a0, dur)); m = p * N; mi = int(m)
    rh = (y1 - y0 - 80) / n; bx0, bx1 = x0 + 40, x1 - 40
    txt(img, ((x0 + x1) / 2, y0 + 10), f'MONTH {mi}', 54, 'Black', None, 'mm')
    for i, s in enumerate(ser):
        y = y0 + 90 + rh * i; bal = s['balances']; k = min(mi, len(bal) - 1); b = lerp(bal[k], bal[min(k + 1, len(bal) - 1)], m - mi) if k < len(bal) - 1 else bal[k]
        start = bal[0]; col = s['color']
        txt(img, (bx0, y + 22), s['label'], 40, 'Black', col if not TH['paper'] else TH['txt'], 'lm')
        cv = Cv((bx0 - 3, y + 62, bx1 + 3, y + 128)); cv.rrect((bx0, y + 70, bx1, y + 118), 24, fill=rgba(TH['txt'], 26))
        if b > 1:
            cv.rrect((bx0, y + 70, bx0 + max(48, (bx1 - bx0) * b / start), y + 118), 24, fill=rgba(col)); cv.paste(img)
        else:
            cv.rrect((bx0, y + 70, bx1, y + 118), 24, fill=rgba(GREEN)); cv.paste(img)
        done = b <= 1
        txt(img, (bx0, y + 152), 'DEBT-FREE!' if done else f'{money(b)} left', 34, 'Black', GREEN if done else None, 'lm')
        ic = s['interest'][min(mi, len(s['interest']) - 1)]
        txt(img, (bx1, y + 152), f'Interest paid: {money(ic)}', 34, 'Bold', CORAL if not TH['paper'] else (180, 50, 40), 'rm')


def el_checklist(img, t, S, el, R):
    x0, y0, x1, y1 = el.get('region', CONTENT); items = el['items']; n = len(items); rh = min(112, (y1 - y0) / n)
    for i, it in enumerate(items):
        p = e_out(prog(t, R(it['at']), .45)); al = clamp(p)
        if al <= 0:
            continue
        y = y0 + rh * (i + .5); col = it.get('color', GREEN if it.get('ok', True) else CORAL)
        panel(img, (x0 + 50 * (1 - al), y - rh / 2 + 8, x1, y + rh / 2 - 8), col, al, 26)
        icon(img, 'check' if it.get('ok', True) else 'x', x0 + 50 * (1 - al) + 64, y, 30, NAVY, col, al)
        txt(img, (x0 + 50 * (1 - al) + 124, y), it['text'], el.get('size', 36), 'Bold', None, 'lm', al)
        if it.get('sub'):
            sub(img, (x1 - 36, y), it['sub'], 26, 'Medium', 'rm', al)


def el_flow(img, t, S, el, R):
    nodes = {n['id']: n for n in el['nodes']}; d = ImageDraw.Draw(img, 'RGBA')
    for a_, b_, at in el.get('arrows', []):
        na, nb = nodes[a_], nodes[b_]; q = e_out(prog(t, R(at), .5))
        if q <= 0:
            continue
        p0 = (na['x'] + na['w'] / 2 if nb['x'] > na['x'] else na['x'], na['y']); p0 = (na['x'] + na['w'], na['y'] + na['h'] / 2) if nb['x'] > na['x'] + na['w'] / 2 else (na['x'] + na['w'] / 2, na['y'] + na['h'])
        p1 = (nb['x'], nb['y'] + nb['h'] / 2) if nb['x'] > na['x'] + na['w'] / 2 else (nb['x'] + nb['w'] / 2, nb['y'])
        pts = [p0, ((p0[0] + p1[0]) / 2, p0[1]), ((p0[0] + p1[0]) / 2, p1[1]), p1] if abs(p0[1] - p1[1]) > 4 and p0[0] != p1[0] and nb['x'] > na['x'] + na['w'] / 2 else [p0, p1]
        d.line(pts, fill=rgba(TH['txt'], 90 * q), width=6, joint='curve')
        segs = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]; tot = sum(segs)
        if t > R(at) + .5 and tot > 0:
            cvd = Cv((0, 0, W, H), s=1)
            for k in range(3):
                u = ((t - R(at)) * .5 + k / 3) % 1; dist = u * tot
                for i, sl in enumerate(segs):
                    if dist <= sl:
                        f = dist / sl; x = lerp(pts[i][0], pts[i + 1][0], f); y = lerp(pts[i][1], pts[i + 1][1], f); cvd.ellipse((x - 11, y - 11, x + 11, y + 11), fill=rgba(el.get('dotcolor', GREEN))); break
                    dist -= sl
            cvd.paste(img)
    for nd in el['nodes']:
        p = e_back(prog(t, R(nd['at']), .55)); al = clamp(p)
        if al <= 0:
            continue
        box = (nd['x'], nd['y'] + 30 * (1 - al), nd['x'] + nd['w'], nd['y'] + nd['h'] + 30 * (1 - al)); col = nd.get('color', GREEN)
        panel(img, box, col, al, 28)
        if nd.get('icon'):
            icon(img, nd['icon'], box[0] + 64, (box[1] + box[3]) / 2, 34, NAVY, col, al)
        tx = box[0] + (124 if nd.get('icon') else 30)
        if nd.get('sub'):
            txt(img, (tx, (box[1] + box[3]) / 2 - 24), nd['title'], nd.get('size', 32), 'Bold', None, 'lm', al); text(img, (tx, (box[1] + box[3]) / 2 + 28), nd['sub'], nd.get('subsize', 46), 'Black', col if not TH['paper'] else TH['txt'], 'lm', al)
        else:
            txt(img, (tx, (box[1] + box[3]) / 2), nd['title'], nd.get('size', 32), 'Bold', None, 'lm', al)


def el_statement(img, t, S, el, R):
    x0, y0, x1, y1 = el.get('region', (200, 300, 1720, 950)); rows = el['rows']; rh = el.get('rowh', 62)
    box = (x0, y0, x1, y0 + 70 + rh * len(rows) + 40)
    shadow(img, box, 22, 28, 120); cv = Cv((x0 - 3, y0 - 3, x1 + 3, box[3] + 3)); cv.rrect(box, 22, fill=rgba((253, 252, 247))); cv.paste(img)
    text(img, (x0 + 40, y0 + 38), el.get('title', 'BANK STATEMENT'), 26, 'Black', (90, 100, 120), 'lm'); text(img, (x1 - 40, y0 + 38), el.get('period', ''), 24, 'Medium', (120, 130, 150), 'rm')
    d = ImageDraw.Draw(img, 'RGBA')
    for i, r in enumerate(rows):
        p = e_out(prog(t, R(r['at']), .4)); y = y0 + 70 + rh * i
        if p <= 0:
            continue
        hp = e_out(prog(t, R(r['hl']), .4)) if r.get('hl') else 0
        if hp > 0:
            d.rectangle([x0 + 10, y + 4, x1 - 10, y + rh - 4], fill=rgba(CORAL, 70 * hp))
            pill(img, x1 - 330, y + rh / 2, r.get('flag', 'LEAK'), 20, CORAL, WHITE, padx=16, h=34, alpha=hp)
        text(img, (x0 + 40, y + rh / 2), r['date'], 26, 'Medium', (110, 120, 140), 'lm', p)
        text(img, (x0 + 200, y + rh / 2), r['merchant'], 30, 'SemiBold', (30, 40, 60), 'lm', p)
        text(img, (x1 - 40, y + rh / 2), r['amount'], 30, 'Bold', (150, 40, 30) if hp > 0 else (30, 40, 60), 'rm', p)
        d.line([(x0 + 30, y + rh), (x1 - 30, y + rh)], fill=(225, 228, 235, int(255 * p)), width=1)


def el_callout(img, t, S, el, R):
    x0, y0, x1, y1 = el.get('region', CONTENT); a0 = R(el['at']); p = e_back(prog(t, a0, .55)); al = clamp(p)
    if al <= 0:
        return
    col = el.get('color', GOLD); size = el.get('size', 54); lines = el['lines'] if 'lines' in el else [el['text']]
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 + 24 * (1 - al); wmax = max(text_w(l, size, 'Black') for l in lines) + 100; hh = len(lines) * size * 1.3 + 50
    cv = Cv((cx - wmax / 2 - 4, cy - hh / 2 - 4, cx + wmax / 2 + 4, cy + hh / 2 + 4)); cv.rrect((cx - wmax / 2, cy - hh / 2, cx + wmax / 2, cy + hh / 2), 30, fill=rgba(col)); cv.paste(img, al)
    for i, l in enumerate(lines):
        text(img, (cx, cy - hh / 2 + 25 + size * .65 + i * size * 1.3), l, size, 'Black', el.get('fg', NAVY), 'mm', al)


def el_steps(img, t, S, el, R):
    x0, y0, x1, y1 = el.get('region', CONTENT); items = el['items']; n = len(items); gap = 20; w = (x1 - x0 - gap * (n - 1)) / n
    for i, it in enumerate(items):
        p = e_out(prog(t, R(it['at']), .5)); al = clamp(p)
        if al <= 0:
            continue
        x = x0 + i * (w + gap) + 40 * (1 - al); col = it.get('color', GREEN)
        cv = Cv((x - 3, y0 - 3, x + w + 30, y1 + 3)); pts = [(x, y0), (x + w - 40, y0), (x + w, (y0 + y1) / 2), (x + w - 40, y1), (x, y1)] if i else [(x, y0), (x + w - 40, y0), (x + w, (y0 + y1) / 2), (x + w - 40, y1), (x, y1)]
        cv.poly(pts, fill=rgba(col)); cv.paste(img, al)
        text(img, (x + 34, y0 + 56), it['title'], it.get('tsize', 34), 'Black', NAVY, 'lm', al)
        yy = y0 + 112
        for l in wrap(it.get('sub', ''), 26, w - 100, 'SemiBold'):
            text(img, (x + 34, yy), l, 26, 'SemiBold', NAVY, 'lm', al); yy += 36


def el_brand(img, t, S, el, R):
    a0 = R(el['at']); p = e_back(prog(t, a0 - .2, .9)); al = clamp(p); cy = 430 + 80 * (1 - al) if el.get('layout', 'center') == 'center' else 430
    w1, w2 = text_w('Broke', 170, 'Black'), text_w('Balance', 170, 'Black'); arrow = 170; tot = w1 + arrow + w2; x0 = 960 - tot / 2
    text(img, (x0, cy), 'Broke', 170, 'Black', CORAL, 'lm', al); ap = e_out(prog(t, a0 + .5, .6)); ax = x0 + w1 + 20
    cvv = Cv((ax - 4, cy - 50, ax + arrow, cy + 50)); cvv.line([(ax + 10, cy), (ax + 10 + (arrow - 76) * ap, cy)], rgba(TH['txt']), 12)
    if ap > .6:
        cvv.poly([(ax + arrow - 92, cy - 34), (ax + arrow - 50, cy), (ax + arrow - 92, cy + 34)], fill=rgba(TH['txt']))
    cvv.paste(img); text(img, (x0 + w1 + arrow, cy), 'Balance', 170, 'Black', GREEN, 'lm', al)
    lp = e_out(prog(t, a0 + .4, .9)); cv = Cv((960 - 600, cy + 110, 960 + 600, cy + 134)); cv.rrect((960 - 560 * lp, cy + 116, 960 + 560 * lp, cy + 126), 5, fill=rgba(GOLD)); cv.paste(img)
    sp = e_out(prog(t, R(el.get('sub_at', el['at'])) + .3, .7))
    pill(img, 960, cy + 230 - 16 * (1 - sp), el['pill'], 46, WHITE if not TH['paper'] else NAVY, NAVY if not TH['paper'] else WHITE, padx=44, h=86, alpha=sp)
    text(img, (960, cy + 340 - 16 * (1 - sp)), el['line'], 30, 'Bold', TH['sub'] if TH['paper'] else LIGHT, 'mm', sp)


def el_cta(img, t, S, el, R):
    a0 = R(el['at']); p = e_back(prog(t, a0, .9)); al = clamp(p)
    if al <= 0:
        return
    yy = 470 + 40 * (1 - al)
    txt(img, (960, yy - 190), el.get('head', 'Enjoyed this?'), 84, 'Black', None, 'mm', al)
    bw = 560; cv = Cv((960 - bw / 2 - 6, yy - 60, 960 + bw / 2 + 120, yy + 70)); cv.rrect((960 - bw / 2, yy - 56, 960 + bw / 2, yy + 56), 56, fill=rgba((235, 40, 40)))
    cv.poly([(960 - bw / 2 + 56, yy - 22), (960 - bw / 2 + 56, yy + 22), (960 - bw / 2 + 92, yy)], fill=rgba(WHITE)); cv.paste(img, al)
    text(img, (960 + 24, yy), 'SUBSCRIBE', 52, 'Black', WHITE, 'mm', al)
    txt(img, (960, yy + 130), el['question'], 38, 'SemiBold', None, 'mm', al * e_out(prog(t, a0 + 1.6, .6)))
    if el.get('next'):
        pill(img, 960, yy + 230, 'NEXT:  ' + el['next'], 32, GREEN, NAVY, padx=40, h=68, alpha=al * e_out(prog(t, a0 + 2.6, .6)))


KINDS = dict(title=el_title, bullets=el_bullets, bars=el_bars, columns=el_columns, donut=el_donut, line=el_line, table=el_table, counter=el_counter,
             gauge=el_gauge, cards=el_cards, compare=el_compare, calendar=el_calendar, race=el_race, checklist=el_checklist, flow=el_flow,
             statement=el_statement, callout=el_callout, steps=el_steps, brand=el_brand, cta=el_cta)
DEFAULT_SFX = dict(title='pop', bullets='tick', bars='bubble', columns='bubble', donut='bubble', line='slide', table='tick', counter='coin', gauge='bubble',
                   cards='thud', compare='slide', calendar='tick', race='slide', checklist='ding', flow='pop', statement='tick', callout='thud', steps='pop', brand='sparkle', cta='cash')


def E(kind, at, **kw):
    d = dict(kind=kind, at=at); d.update(kw); return d


# ---------------------------------------------------------------- scene factory
def make_render(sc, style):
    def render(img, t, S):
        global TH
        TH = THEMES[style.get('theme', 'night')]
        background(img, t, sc.get('bg', style.get('bg', {})))
        R = lambda ref: parse_ref(ref, S)
        h = sc.get('header')
        if h:
            h = dict(h); h['style'] = style.get('header', 'pill'); draw_header(img, t, h, R(h.get('at', sc['segs'][0][0])))
        for el in sc.get('els', []):
            a0 = R(el['at']); fi = e_out(prog(t, a0 - .05, .3)) if el['kind'] not in ('brand',) else 1.0
            fo = 1 - e_inout(prog(t, R(el['until']), .35)) if el.get('until') else 1.0
            al = fi * fo
            if al <= .003 and t < a0 + 5:
                if t < a0 - .05:
                    continue
            if al <= .003:
                continue
            fn = KINDS[el['kind']]
            if al >= .999:
                fn(img, t, S, el, R)
            else:
                tmp = img.copy(); fn(tmp, t, S, el, R); img.paste(Image.blend(img, tmp, al), (0, 0))
    return render


def sfx_events(sc, S):
    R = lambda ref: parse_ref(ref, S); ev = []
    for el in sc.get('els', []):
        sf = el.get('sfx', DEFAULT_SFX.get(el['kind']))
        if sf is None:
            continue
        items = el.get('items') or el.get('rows') or el.get('marks') or el.get('nodes') or []
        times = [R(it['at']) for it in items if isinstance(it, dict) and 'at' in it]
        if el['kind'] == 'compare':
            times = [R(el['left']['at']), R(el['right']['at'])]
        if not times:
            times = [R(el['at'])]
        for i, tm in enumerate(times):
            k = sf if (i % 2 == 0 or sf not in ('tick', 'bubble', 'coin')) else sf + '2'
            ev.append((tm, k))
    for ref, k in sc.get('sfx', []):
        ev.append((R(ref), k))
    return ev


def install(spec, style, scenes_module):
    """Wire an episode into build.py via the scenes module registry."""
    scenes_module.SCRIPT = [(sc['id'], sc['segs']) for sc in spec]
    scenes_module.RENDER = {sc['id']: make_render(sc, style) for sc in spec}
    byid = {sc['id']: sc for sc in spec}

    def events(sid, S):
        return [(max(0, x), k) for x, k in sfx_events(byid[sid], S)]
    scenes_module.events = events
