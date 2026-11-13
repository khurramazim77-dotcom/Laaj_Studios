#!/usr/bin/env python3
"""usage: python episode_build.py ep2 audio|preview t..|render|thumb"""
import os, sys, importlib, math
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'episodes'))
name = sys.argv[1]; cmd = sys.argv[2]
ep = importlib.import_module(name)
M = ep.META
os.environ['B2B_OUT'] = f'{ROOT}/episodes/{name}'
os.makedirs(os.environ['B2B_OUT'], exist_ok=True)
os.environ['B2B_WORK'] = f"/tmp/claude-0/-home-user-Laaj-Studios/864a7258-c942-549a-bb5d-f0b0a13dd3aa/scratchpad/{name}"
os.environ['B2B_FINAL'] = M['final']; os.environ['B2B_MUSIC'] = str(M['music']); os.environ['B2B_SPEED'] = str(M.get('voice_speed', 1.0))
import lib
lib.SPEED = float(M.get('gfx_speed', 1.6)); lib.BG = float(M.get('bg_speed', 2.0))
import build, scenes, engine
engine.install(ep.SPEC, ep.STYLE, scenes)
build.TRANS = ep.STYLE['trans']

def thumb():
    from lib import W, H, bg_soft, Cv, rgba, text, pill, icon, fade_overlay, NAVY, NAVY2, WHITE, GOLD
    from PIL import Image
    T = M['thumb']; img = Image.new('RGBA', (W, H), (0, 0, 0, 255))
    engine.TH = engine.THEMES['night']
    engine.background(img, 3.0, T.get('bg', ep.STYLE['bg']))
    fade_overlay(img, NAVY, .2)
    y = T.get('y0', 240)
    for s, size, col in T['lines']:
        text(img, (110, y), s, size, 'Black', col, 'lm'); y += size * 1.05 + 14
    cx, cy = 1450, 540
    cv = Cv((cx - 340, cy - 340, cx + 340, cy + 340), s=2); cv.ellipse((cx - 300, cy - 300, cx + 300, cy + 300), fill=rgba(T['accent'])); cv.paste(img)
    icon(img, T['icon'], cx, cy, 250, WHITE, None)
    text(img, (cx, cy + 400), T.get('tag', ''), 54, 'Black', WHITE, 'mm')
    pill(img, 330, 960, 'BROKE → BALANCE', 40, WHITE, NAVY, padx=44, h=84)
    img.convert('RGB').resize((1280, 720), Image.LANCZOS).save(f"{os.environ['B2B_OUT']}/thumbnail.png"); print('thumb ok')

if cmd == 'audio':
    build.do_audio()
elif cmd == 'preview':
    os.makedirs(f'{build.WORK}/prev', exist_ok=True)
    for tt in sys.argv[3:]:
        build.render_frame(int(float(tt) * 30)).save(f'{build.WORK}/prev/f_{float(tt):06.1f}.png'); print('saved', tt)
elif cmd == 'render':
    build.do_render()
elif cmd == 'thumb':
    thumb()
elif cmd == 'times':
    import json
    T = json.load(open(f'{build.WORK}/timeline.json'))
    for s in T['tl']:
        print(s['sid'], round(s['start'], 1), {k: (round(v[0], 1), round(v[1], 1)) for k, v in s['S'].items()})
