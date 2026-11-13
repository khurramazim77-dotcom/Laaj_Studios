#!/usr/bin/env python3
"""Vertical (1080x1920) YouTube Shorts cut of Episode 1. usage: python shorts_build.py audio|preview t..|render"""
import os, sys, json, math, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
os.environ['B2B_WORK'] = os.environ.get('B2B_SHORTS_WORK', '/tmp/claude-0/-home-user-Laaj-Studios/864a7258-c942-549a-bb5d-f0b0a13dd3aa/scratchpad/shorts')
sys.path.insert(0, HERE)
import lib
lib.W, lib.H = 1080, 1920
from lib import *
import numpy as np
from scipy.io import wavfile
import build as B
from scenes import TAKE_HOME, SPLIT

FPS_ = 30
SCRIPT = [
    ('k1', "You get paid, and by the twentieth, it's gone.", "You get paid, and by the 20th, it's gone."),
    ('k1b', "Rent, subscriptions, and impulse buys take everything.", None),
    ('k2', "Fix it with the fifty, thirty, twenty rule.", "Fix it with the 50/30/20 rule."),
    ('k3', "Start with your take-home pay. Say, three thousand dollars.", "Start with your take-home pay. Say, $3,000."),
    ('k4', "Fifty percent, fifteen hundred, goes to needs: rent, groceries, and bills.", "50%, $1,500, goes to needs: rent, groceries, and bills."),
    ('k5', "Thirty percent, nine hundred, goes to wants: fun, shopping, and eating out.", "30%, $900, goes to wants: fun, shopping, and eating out."),
    ('k6', "Twenty percent, six hundred, goes to savings and debt payoff.", "20%, $600, goes to savings and debt payoff."),
    ('k7', "Pay yourself first. Automate that savings transfer on payday.", None),
    ('k8', "Needs over fifty percent? That's not failure, it's information.", "Needs over 50%? That's not failure, it's information."),
    ('k9', "Subscribe to Broke to Balance for the full breakdown.", None),
]


def timeline():
    S, clips, caps = {}, [], []
    t = 0.5
    for k, say, show in SCRIPT:
        x = B.tts(say, k)
        d = len(x) / B.SR
        S[k] = (t, d); clips.append((t, x)); caps.append((t, t + d, show or say))
        t += d + 0.28
    total = t - 0.28 + 1.6
    return S, clips, caps, total


def events(S):
    a = lambda k: S[k][0]
    ev = [(0.05, 'sting')]
    t0 = a('k1b') + 0.1; sp = a('k2') - t0 - 0.3
    ev += [(t0 + sp * i / 6, 'pop') for i in range(6)]
    ev += [(a('k2') - 0.1, 'whoosh'), (a('k2') + 0.3, 'ching'), (a('k3') - 0.1, 'whoosh'),
           (a('k4') + .1, 'swell'), (a('k5') + .1, 'swell'), (a('k6') + .1, 'swell'), (a('k6') + 3.2, 'ching'),
           (a('k7') - 0.1, 'whoosh'), (a('k7') + 1.5, 'pop'), (a('k8') - 0.1, 'whoosh'), (a('k9') - 0.1, 'whoosh'), (a('k9') + .4, 'ching')]
    return ev


def do_audio():
    S, clips, caps, total = timeline()
    n = int((total + 1) * B.SR)
    voice = np.zeros(n, np.float32)
    for t0, x in clips:
        i = int(t0 * B.SR); voice[i:i + len(x)] += x
    mus = B.music(total + 1, drums_from=1.0, mel_from=1.0)
    env = np.convolve(np.abs(voice), np.ones(int(.25 * B.SR)) / int(.25 * B.SR), 'same')
    env = np.convolve(np.clip(env / 0.08, 0, 1), np.ones(int(.35 * B.SR)) / int(.35 * B.SR), 'same')
    mus = mus * (1 - 0.6 * env).astype(np.float32)
    fo = int(1.6 * B.SR); e = int(total * B.SR)
    mus[e - fo:e] *= np.linspace(1, 0, fo); mus[e:] = 0
    mix = voice + mus * 0.9
    for t0, kind in events(S):
        x = B.sfx(kind); i = int(t0 * B.SR)
        if 0 <= i and i + len(x) < n:
            mix[i:i + len(x)] += x.astype(np.float32)
    mix = np.tanh(mix * 0.9) / 0.9 * 0.9
    wavfile.write(f'{B.WORK}/mix_raw.wav', B.SR, (np.clip(mix, -1, 1) * 32767).astype(np.int16))
    B.sh(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{B.WORK}/mix_raw.wav', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=9', '-ar', '44100', '-ac', '2', f'{B.WORK}/mix.wav'])
    chunks = []
    for a, b, txt in caps:
        parts = B.split_caption(txt, 30)
        tot = sum(len(p) for p in parts); t = a
        for p in parts:
            d = (b - a) * len(p) / tot; chunks.append((t, t + d, p)); t += d
    json.dump(dict(S=S, total=total, caps=chunks), open(f'{B.WORK}/timeline.json', 'w'))
    with open(f'{OUT}/shorts_captions.srt', 'w') as f:
        for i, (a, b, txt) in enumerate(chunks, 1):
            f.write(f'{i}\n{B.srt_time(a)} --> {B.srt_time(b)}\n{txt}\n\n')
    print(f'shorts total {total:.1f}s, words', sum(len(s[1].split()) for s in SCRIPT))


# ------------------------------------------------------------------ visuals (1080 x 1920)
CX = 540


def win(t, a, b, fi=0.3, fo=0.3, last=False):
    p = (clamp((t - a) / fi) if fi > 0 else 1.0) * (1.0 if last else clamp((b - t) / fo))
    return e_out(p) if p < 1 else 1.0


def sec_hook(img, t, S):
    a, d = (lambda k: S[k][0]), (lambda k: S[k][1])
    text(img, (CX, 330), 'Why are you', 76, 'Black', WHITE, 'mm')
    text(img, (CX, 415), 'broke by the 20th?', 76, 'Black', CORAL, 'mm')
    pin = e_back(prog(t, 0.1, 0.8))
    cy = 900 + lerp(-600, 0, pin)
    box = (80, cy - 210, 1000, cy + 210)
    card(img, box, 36, WHITE)
    cvh = Cv((box[0], box[1], box[2], box[1] + 100))
    cvh.rrect((box[0], box[1], box[2], box[1] + 98), 36, fill=rgba(GREEN)); cvh.rrect((box[0], box[1] + 60, box[2], box[1] + 98), 0, fill=rgba(GREEN)); cvh.paste(img)
    chips = [('Rent', 1000), ('Groceries', 450), ('Subscriptions', 85), ('Delivery', 210), ('Impulse order', 160), ('Everything else', 1095)]
    t0, span = a('k1b') + 0.1, a('k2') - (a('k1b') + 0.1) - 0.3
    spent, sched = 0.0, []
    for i, (n, am) in enumerate(chips):
        ts = t0 + span * i / len(chips)
        spent += am * e_out(prog(t, ts, 0.5)); sched.append((n, am, ts))
    bal = max(0, TAKE_HOME - spent)
    day = 1 + int(19 * prog(t, t0, span))
    text(img, (box[0] + 44, box[1] + 50), 'PAYDAY', 40, 'ExtraBold', NAVY, 'lm')
    text(img, (box[2] - 44, box[1] + 50), f'DAY {day}', 38, 'ExtraBold', NAVY, 'rm')
    text(img, (CX, box[1] + 148), 'YOUR BALANCE', 28, 'Bold', GREY, 'mm')
    fr = clamp(bal / TAKE_HOME)
    col = lerpc(CORAL, (214, 150, 0), fr / 0.5) if fr < 0.5 else lerpc((214, 150, 0), GREEN_D, (fr - 0.5) / 0.5)
    text(img, (CX, box[1] + 258), money(bal, True), 132, 'Black', col, 'mm')
    cvb = Cv((120, box[1] + 330, 960, box[1] + 372))
    cvb.rrect((140, box[1] + 342, 940, box[1] + 362), 10, fill=rgba(LIGHT))
    if bal > 1:
        cvb.rrect((140, box[1] + 342, 140 + 800 * bal / TAKE_HOME, box[1] + 362), 10, fill=rgba(col))
    cvb.paste(img)
    for i, (n, am, ts) in enumerate(sched):
        p = prog(t, ts, 1.1)
        if 0 < p < 1:
            side = -1 if i % 2 == 0 else 1
            x = CX + side * 170
            y = cy - 232 - 100 * e_out(p)
            pill(img, x, y, f'−{money(am)}  {n}', 34, CORAL, WHITE, padx=26, h=62, alpha=1 - clamp((p - .4) / .5))


def sec_title(img, t, S):
    a = lambda k: S[k][0]
    p = e_back(prog(t, a('k2') - 0.1, 0.7))
    text(img, (CX, 700 + 40 * (1 - clamp(p))), '50/30/20', 188, 'Black', WHITE, 'mm', clamp(p))
    pill(img, CX, 900, 'THE BUDGET RULE', 44, GOLD, NAVY, padx=44, h=82, alpha=e_out(prog(t, a('k2') + 0.3, 0.5)))
    text(img, (CX, 1030), 'for every paycheck', 52, 'SemiBold', LIGHT, 'mm', e_out(prog(t, a('k2') + 0.6, 0.5)))


def sec_donut(img, t, S):
    a, d = (lambda k: S[k][0]), (lambda k: S[k][1])
    text(img, (CX, 300), 'Take-home: $3,000', 66, 'Black', WHITE, 'mm', e_out(prog(t, a('k3'), 0.5)))
    cx, cy, R, r = CX, 730, 330, 208
    cv = Cv((cx - R - 10, cy - R - 10, cx + R + 10, cy + R + 10), s=3)
    cv.ellipse((cx - R, cy - R, cx + R, cy + R), fill=rgba(WHITE, 28))
    for i, (sid, a0) in enumerate((('k4', 0), ('k5', 180), ('k6', 288))):
        name, frac, col, ic, amt = SPLIT[i]
        p = e_inout(prog(t, a(sid) + 0.1, min(1.2, d(sid) * .6)))
        if p > .003:
            cv.pie((cx - R, cy - R, cx + R, cy + R), a0 - 90 + .8, max(a0 - 89, a0 - 90 + 360 * frac * p - .8), rgba(col))
    cv.d.ellipse(cv.B((cx - r, cy - r, cx + r, cy + r)), fill=(0, 0, 0, 0))
    cv.ellipse((cx - r, cy - r, cx + r, cy + r), fill=rgba(NAVY))
    cv.paste(img)
    text(img, (CX, cy - 20), '$3,000', 78, 'Black', WHITE, 'mm')
    text(img, (CX, cy + 50), 'per month', 28, 'Medium', GREY, 'mm')
    for i, (name, frac, col, ic, amt) in enumerate(SPLIT):
        sid = ('k4', 'k5', 'k6')[i]
        p = e_out(prog(t, a(sid) + .15, .5))
        if p <= 0:
            continue
        y = 1150 + i * 118
        box = (70 + 40 * (1 - p), y - 54, 1010 + 40 * (1 - p), y + 54)
        card(img, box, 28, WHITE, int(28 * p), shad=False, outline=rgba(col, 220 * p))
        icon(img, ic, box[0] + 70, y, 34, NAVY, col, p)
        text(img, (box[0] + 130, y), f'{int(frac * 100)}%  {name.split(" ")[0]}', 40, 'ExtraBold', col, 'lm', p)
        dp = e_out(prog(t, a(sid) + .3, .9))
        text(img, (box[2] - 34, y), money(amt * dp), 52, 'Black', WHITE, 'rm', p)


def sec_tip(img, t, S):
    a = lambda k: S[k][0]
    p0 = e_out(prog(t, a('k7'), .5))
    pill(img, CX, 270, 'BEST HABIT', 30, GREEN, NAVY, padx=30, h=56, alpha=p0)
    text(img, (CX, 380), 'Pay yourself first', 84, 'Black', WHITE, 'mm', p0)
    card(img, (240, 520, 840, 700), 32, WHITE, int(255 * p0))
    text(img, (CX, 570), 'PAYCHECK ARRIVES', 24, 'Bold', GREY, 'mm', p0)
    text(img, (CX, 640), '+ $3,000', 70, 'Black', GREEN_D, 'mm', p0)
    q = e_out(prog(t, a('k7') + .7, .6))
    dd = ImageDraw.Draw(img, 'RGBA')
    for tx in (290, 790):
        dd.line([(CX, 700), (CX, 770), (tx, 770), (tx, 850)], fill=rgba(WHITE, 80 * q), width=6, joint='curve')
    if q > 0:
        for tx, col in ((290, GREEN), (790, (140, 185, 255))):
            cvd = Cv((0, 0, W, H), s=1)
            for k in range(4):
                u = ((t - a('k7') - .9) * .6 + k / 4) % 1.0
                if t < a('k7') + .9:
                    continue
                pts = [(CX, 700), (CX, 770), (tx, 770), (tx, 850)]
                segs = [math.dist(pts[i], pts[i + 1]) for i in range(3)]; dist = u * sum(segs)
                for i, sl in enumerate(segs):
                    if dist <= sl:
                        f = dist / sl; cvd.ellipse((lerp(pts[i][0], pts[i + 1][0], f) - 12, lerp(pts[i][1], pts[i + 1][1], f) - 12, lerp(pts[i][0], pts[i + 1][0], f) + 12, lerp(pts[i][1], pts[i + 1][1], f) + 12), fill=rgba(col)); break
                    dist -= sl
            cvd.paste(img)
    for (x0, x1, ttl, amt, col, ic) in ((60, 520, 'Auto-save', '$600', GREEN, 'piggy'), (560, 1020, 'Left to spend', '$2,400', (140, 185, 255), 'cart')):
        card(img, (x0, 860, x1, 1100), 30, WHITE, int(40 * q), shad=False, outline=rgba(col, 230 * q))
        icon(img, ic, (x0 + x1) / 2, 930, 38, NAVY, col, q)
        text(img, ((x0 + x1) / 2, 1005), ttl, 34, 'Bold', WHITE, 'mm', q)
        text(img, ((x0 + x1) / 2, 1062), amt, 56, 'Black', col, 'mm', q)
    pill(img, CX, 1200, 'Savings leave BEFORE you spend', 36, GOLD, NAVY, padx=40, h=76, alpha=e_out(prog(t, a('k7') + 2.2, .5)))


def sec_info(img, t, S):
    a = lambda k: S[k][0]
    p0 = e_out(prog(t, a('k8'), .5))
    text(img, (CX, 330), 'Needs over 50%?', 86, 'Black', WHITE, 'mm', p0)
    cx, cy, R = CX, 760, 230
    g = e_out(prog(t, a('k8') + .3, 1.0))
    cv = Cv((cx - R - 40, cy - R - 40, cx + R + 40, cy + R + 40), s=3)
    cv.arc((cx - R, cy - R, cx + R, cy + R), 0, 360, rgba(WHITE, 40), 44)
    cv.arc((cx - R, cy - R, cx + R, cy + R), -90, -90 + 360 * .60 * g, rgba(CORAL), 44)
    cv.paste(img)
    text(img, (CX, cy - 20), f'{int(60 * g)}%', 120, 'Black', WHITE, 'mm')
    text(img, (CX, cy + 70), 'of take-home', 32, 'Medium', GREY, 'mm')
    text(img, (CX, 1130), 'Not failure.', 64, 'Black', CORAL, 'mm', e_out(prog(t, a('k8') + 2.0, .5)))
    text(img, (CX, 1210), "It's information.", 64, 'Black', GREEN, 'mm', e_out(prog(t, a('k8') + 2.9, .5)))
    for i, lab in enumerate(('Trim', 'Negotiate', 'Earn more')):
        pill(img, 220 + i * 320, 1330, lab, 32, WHITE, NAVY, padx=26, h=62, alpha=e_out(prog(t, a('k8') + 3.4 + i * .3, .4)))


def sec_cta(img, t, S):
    a = lambda k: S[k][0]
    p = e_back(prog(t, a('k9') - 0.1, .8))
    al = clamp(p)
    text(img, (CX, 560 + 40 * (1 - al)), 'Broke', 130, 'Black', CORAL, 'mm', al)
    text(img, (CX, 700 + 40 * (1 - al)), '↓', 90, 'Black', WHITE, 'mm', al)
    text(img, (CX, 840 + 40 * (1 - al)), 'Balance', 130, 'Black', GREEN, 'mm', al)
    text(img, (CX, 1000), 'Full video: How to Budget Your Paycheck', 38, 'SemiBold', LIGHT, 'mm', e_out(prog(t, a('k9') + .5, .5)))
    q = e_back(prog(t, a('k9') + 1.0, .7)); aq = clamp(q)
    cv = Cv((CX - 330, 1070, CX + 330, 1230))
    cv.rrect((CX - 300, 1090, CX + 300, 1200), 55, fill=rgba((235, 40, 40)))
    cv.poly([(CX - 240, 1128), (CX - 240, 1162), (CX - 208, 1145)], fill=rgba(WHITE))
    cv.paste(img, aq)
    text(img, (CX + 24, 1145), 'SUBSCRIBE', 52, 'Black', WHITE, 'mm', aq)


def frame(i):
    from PIL import Image
    T = json.load(open(f'{B.WORK}/timeline.json')) if not hasattr(frame, 'T') else frame.T
    frame.T = T
    S = {k: tuple(v) for k, v in T['S'].items()}
    t = i / 30
    a = lambda k: S[k][0]
    img = Image.new('RGBA', (W, H), (0, 0, 0, 255))
    bg_soft(img, t, NAVY, NAVY2, GREEN, 11)
    money_rain(img, t + 3, 12, 31, 0.40)
    fade_overlay(img, NAVY, 0.30)
    secs = [(sec_hook, 0, a('k2') - 0.05), (sec_title, a('k2') - 0.1, a('k3') - 0.05), (sec_donut, a('k3') - 0.1, a('k7') - 0.05),
            (sec_tip, a('k7') - 0.1, a('k8') - 0.05), (sec_info, a('k8') - 0.1, a('k9') - 0.05), (sec_cta, a('k9') - 0.1, 1e9)]
    for fn, t0, t1 in secs:
        al = win(t, t0, t1, 0.0 if t0 == 0 else 0.3, 0.3, last=(t1 > 1e8))
        if al <= 0.003:
            continue
        if al >= 0.999:
            fn(img, t, S)
        else:
            tmp = img.copy(); fn(tmp, t, S); img = Image.blend(img, tmp, al)
    # logo + captions
    chip = Image.new('RGBA', (460, 140), (0, 0, 0, 0))
    logo_chip(chip, 0.95)
    img.paste(chip, (44, 110), chip)
    for a_, b_, txt in T['caps']:
        if a_ - .05 <= t <= b_ + .15:
            f = clamp((t - (a_ - .05)) / .15)
            tw = text_w(txt, 56, 'ExtraBold')
            box = (CX - tw / 2 - 36, 1500, CX + tw / 2 + 36, 1590)
            cvc = Cv((box[0] - 3, box[1] - 3, box[2] + 3, box[3] + 3))
            cvc.rrect(box, 44, fill=rgba((6, 14, 30), 215)); cvc.paste(img, f)
            text(img, (CX, 1545), txt, 56, 'ExtraBold', WHITE, 'mm', f)
            break
    return img.convert('RGB')


def worker(args):
    f0, f1, idx = args
    out = f'{B.WORK}/chunk_{idx:02d}.mp4'
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1080x1920', '-r', '30', '-i', '-',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', '-pix_fmt', 'yuv420p', '-g', '60', out], stdin=subprocess.PIPE)
    for i in range(f0, f1):
        p.stdin.write(frame(i).tobytes())
    p.stdin.close(); p.wait()
    return out


def do_render():
    from multiprocessing import Pool
    T = json.load(open(f'{B.WORK}/timeline.json'))
    nf = int(math.ceil(T['total'] * 30)); per = 150
    jobs = [(f, min(nf, f + per), j) for j, f in enumerate(range(0, nf, per))]
    with Pool(4) as pool:
        for k, _ in enumerate(pool.imap(worker, jobs)):
            print('done', k + 1, '/', len(jobs), flush=True)
    with open(f'{B.WORK}/list.txt', 'w') as f:
        for j in range(len(jobs)):
            f.write(f"file 'chunk_{j:02d}.mp4'\n")
    B.sh(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'{B.WORK}/list.txt', '-c', 'copy', f'{B.WORK}/v.mp4'])
    final = f'{OUT}/Broke_to_Balance_Short_50-30-20.mp4'
    B.sh(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{B.WORK}/v.mp4', '-i', f'{B.WORK}/mix.wav', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', final])
    print('wrote', final)


if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'audio':
        do_audio()
    elif c == 'preview':
        os.makedirs(f'{B.WORK}/prev', exist_ok=True)
        for tt in sys.argv[2:]:
            frame(int(float(tt) * 30)).save(f'{B.WORK}/prev/s_{float(tt):05.1f}.png'); print('saved', tt)
    elif c == 'render':
        do_render()
