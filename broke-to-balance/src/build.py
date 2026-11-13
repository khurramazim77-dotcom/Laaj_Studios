#!/usr/bin/env python3
"""Build pipeline: TTS -> timeline -> music/sfx mix -> parallel frame render -> mux.

usage:
  python build.py audio                 # synth voice, timeline.json, mix.wav, captions.srt
  python build.py preview t1 t2 ...     # dump PNG frames at the given seconds
  python build.py render                # render all frames (4 procs) and mux final mp4
"""
import sys, os, json, subprocess, hashlib, wave, math, shutil
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.environ.get('B2B_OUT', os.path.dirname(HERE))
FINAL_NAME = os.environ.get('B2B_FINAL', 'Broke_to_Balance_How_to_Budget_Your_Paycheck.mp4')
MUSIC_VARIANT = int(os.environ.get('B2B_MUSIC', '0'))
WORK = os.environ.get('B2B_WORK', '/tmp/claude-0/-home-user-Laaj-Studios/864a7258-c942-549a-bb5d-f0b0a13dd3aa/scratchpad/b2b')
os.makedirs(WORK, exist_ok=True)
SR = 44100
XF = 0.42
TRANS = ['zoom', 'slide', 'wipe', 'flash', 'slide', 'zoom', 'wipe', 'flash', 'zoom']
TRANS_SFX = {'zoom': 'boom', 'slide': 'slide', 'wipe': 'whip', 'flash': 'sparkle', 'fade': 'tick'}


def sh(cmd, **kw):
    return subprocess.run(cmd, shell=isinstance(cmd, str), check=True, **kw)


# ------------------------------------------------------------------ TTS
_K = None
VOICE = os.environ.get('B2B_VOICE', 'am_michael')
KOKORO_DIR = os.environ.get('B2B_KOKORO', '/tmp/claude-0/-home-user-Laaj-Studios/864a7258-c942-549a-bb5d-f0b0a13dd3aa/scratchpad/kokoro_models')
OWN_VOICE_DIR = os.path.join(OUT, 'narration')   # drop <seg_id>.wav/.mp3/.m4a here to use your own recordings


def _kokoro():
    global _K
    if _K is None:
        from kokoro_onnx import Kokoro
        _K = Kokoro(f'{KOKORO_DIR}/kokoro-v1.0.onnx', f'{KOKORO_DIR}/voices-v1.0.bin')
    return _K


def tts(text, key):
    """Narration for one segment. Uses your own recording if narration/<key>.* exists, else Kokoro neural TTS."""
    os.makedirs(f'{WORK}/tts', exist_ok=True)
    own = [f for f in (os.listdir(OWN_VOICE_DIR) if os.path.isdir(OWN_VOICE_DIR) else []) if f.rsplit('.', 1)[0] == key]
    af = ('highpass=f=70,equalizer=f=200:t=q:w=1:g=1.5,equalizer=f=3200:t=q:w=1.2:g=1.5,'
          'acompressor=threshold=-20dB:ratio=3:attack=5:release=90:makeup=3,aresample=44100')
    if own:
        src = os.path.join(OWN_VOICE_DIR, own[0])
        proc = f'{WORK}/tts/own_{key}.wav'
        sh(['ffmpeg', '-y', '-loglevel', 'error', '-i', src, '-af', af, '-ac', '1', '-ar', str(SR), '-c:a', 'pcm_s16le', proc])
    else:
        h = hashlib.md5((VOICE + text).encode()).hexdigest()[:10]
        raw = f'{WORK}/tts/{key}_{VOICE}_{h}_raw.wav'
        proc = f'{WORK}/tts/{key}_{VOICE}_{h}.wav'
        if not os.path.exists(proc):
            import soundfile as sf
            samples, sr = _kokoro().create(text, voice=VOICE, speed=float(os.environ.get('B2B_SPEED', '1.0')), lang='en-us')
            sf.write(raw, samples, sr)
            sh(['ffmpeg', '-y', '-loglevel', 'error', '-i', raw, '-af', af, '-ac', '1', '-ar', str(SR), '-c:a', 'pcm_s16le', proc])
    sr, x = wavfile.read(proc)
    x = x.astype(np.float32) / 32768
    thr = 0.010
    idx = np.where(np.abs(x) > thr)[0]
    if len(idx):
        a, b = max(0, idx[0] - int(0.03 * SR)), min(len(x), idx[-1] + int(0.10 * SR))
        x = x[a:b]
    return x


# ------------------------------------------------------------------ SFX + music
def env_exp(n, tau):
    return np.exp(-np.arange(n) / (tau * SR))


def sfx(kind):
    if kind == 'pop':
        n = int(0.09 * SR); t = np.arange(n) / SR
        f = 520 + 380 * np.exp(-t * 60)
        return 0.32 * np.sin(2 * np.pi * np.cumsum(f) / SR) * env_exp(n, 0.025)
    if kind == 'ching':
        n = int(0.9 * SR); t = np.arange(n) / SR
        y = (np.sin(2 * np.pi * 1318 * t) + 0.6 * np.sin(2 * np.pi * 1975 * t) + 0.35 * np.sin(2 * np.pi * 2637 * t)) * env_exp(n, 0.22)
        y[:int(0.002 * SR)] *= np.linspace(0, 1, int(0.002 * SR))
        return 0.22 * y
    if kind == 'ding':
        n = int(1.0 * SR); t = np.arange(n) / SR
        return 0.2 * (np.sin(2 * np.pi * 1046 * t) + 0.4 * np.sin(2 * np.pi * 2093 * t)) * env_exp(n, 0.3) * np.minimum(1, t / 0.004)
    if kind == 'swell':
        n = int(0.42 * SR); t = np.arange(n) / SR
        f = 330 + 440 * (t / 0.42) ** 1.5
        env = np.sin(np.pi * t / 0.42) ** 2
        return 0.16 * np.sin(2 * np.pi * np.cumsum(f) / SR) * env
    if kind == 'whoosh':
        n = int(0.6 * SR); t = np.arange(n) / SR
        rng = np.random.default_rng(3)
        x = rng.standard_normal(n)
        b, a = butter(2, [300 / (SR / 2), 3800 / (SR / 2)], 'band')
        x = lfilter(b, a, x)
        env = np.sin(np.pi * np.clip(t / 0.6, 0, 1)) ** 2.2
        return 0.16 * x * env / (np.std(x) + 1e-6)
    if kind == 'sting':
        n = int(2.4 * SR); t = np.arange(n) / SR; y = np.zeros(n)
        for i, f in enumerate((523.25, 659.25, 783.99, 1046.5)):
            o = int(i * 0.09 * SR); tt = t[:n - o]
            y[o:] += (np.sin(2 * np.pi * f * tt) + 0.4 * np.sin(2 * np.pi * 2 * f * tt)) * np.exp(-tt * 2.2) * 0.2
        y += np.sin(2 * np.pi * 55 * t) * np.exp(-t * 3.5) * 0.45
        return y * np.minimum(1, t / 0.004)
    if kind == 'riser':
        n = int(2.4 * SR); t = np.arange(n) / SR; u = t / 2.4
        rng = np.random.default_rng(9)
        b, a = butter(2, [500 / (SR / 2), 6000 / (SR / 2)], 'band')
        nz = lfilter(b, a, rng.standard_normal(n)); nz /= np.std(nz) + 1e-6
        f = 200 + 1800 * u ** 2
        tone = np.sin(2 * np.pi * np.cumsum(f) / SR)
        return (0.10 * nz + 0.07 * tone) * u ** 2.2
    rng = np.random.default_rng(sum(map(ord, kind)))
    def band(x, lo, hi):
        b, a = butter(2, [lo / (SR / 2), hi / (SR / 2)], 'band'); return lfilter(b, a, x)
    if kind in ('tick', 'tick2'):
        n = int(0.04 * SR); t = np.arange(n) / SR; f = 1900 if kind == 'tick' else 1150
        return 0.3 * (np.sin(2 * np.pi * f * t) * np.exp(-t * 150) * 0.8 + band(rng.standard_normal(n), 2500, 9000) * np.exp(-t * 200) * 0.25)
    if kind == 'slide':
        n = int(0.32 * SR); t = np.arange(n) / SR
        x = band(rng.standard_normal(n), 700, 5200); x /= np.std(x) + 1e-6
        return 0.10 * x * np.minimum(1, t / 0.04) * np.exp(-t * 11)
    if kind == 'whip':
        n = int(0.2 * SR); t = np.arange(n) / SR
        x = band(rng.standard_normal(n), 2500, 11000); x /= np.std(x) + 1e-6
        return 0.12 * x * np.sin(np.pi * np.clip(t / 0.2, 0, 1)) ** 1.5
    if kind == 'thud':
        n = int(0.45 * SR); t = np.arange(n) / SR
        f = 58 + 70 * np.exp(-t * 28)
        y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 8) * 0.62
        y += band(rng.standard_normal(n), 120, 900) * np.exp(-t * 70) * 0.10
        return y * np.minimum(1, t / 0.002)
    if kind == 'boom':
        n = int(1.1 * SR); t = np.arange(n) / SR
        b, a = butter(2, 320 / (SR / 2), 'low'); nz = lfilter(b, a, rng.standard_normal(n)); nz /= np.std(nz) + 1e-6
        return (0.16 * nz * np.exp(-t * 3.2) + np.sin(2 * np.pi * 46 * t) * np.exp(-t * 3.6) * 0.5) * np.minimum(1, t / 0.003)
    if kind == 'sparkle':
        n = int(1.2 * SR); t = np.arange(n) / SR; y = np.zeros(n)
        for i, f in enumerate((1318.5, 1568, 1760, 2093, 2349, 2637, 3136)):
            o = int(i * 0.05 * SR); tt = t[:n - o]
            y[o:] += (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * 2 * f * tt)) * np.exp(-tt * 7) * 0.09
        return y
    if kind in ('coin', 'coin2'):
        n = int(0.5 * SR); t = np.arange(n) / SR; f1, f2 = (2349, 3136) if kind == 'coin' else (2637, 3520)
        y = np.sin(2 * np.pi * f1 * t) * np.exp(-t * 24) * 0.7
        o = int(0.07 * SR); tt = t[:n - o]
        y[o:] += np.sin(2 * np.pi * f2 * tt) * np.exp(-tt * 14) * 0.9 + np.sin(2 * np.pi * f2 * 2.76 * tt) * np.exp(-tt * 30) * 0.25
        return 0.17 * y * np.minimum(1, t / 0.002)
    if kind == 'cash':
        n = int(1.2 * SR); t = np.arange(n) / SR
        y = band(rng.standard_normal(n), 400, 2600) * np.exp(-t * 45) * 0.18 + np.sin(2 * np.pi * 230 * t) * np.exp(-t * 35) * 0.28
        o = int(0.06 * SR); tt = t[:n - o]
        y[o:] += (np.sin(2 * np.pi * 1568 * tt) + 0.6 * np.sin(2 * np.pi * 2349 * tt) + 0.35 * np.sin(2 * np.pi * 3136 * tt)) * np.exp(-tt * 4.5) * 0.17
        return y
    if kind in ('bubble', 'bubble2'):
        n = int(0.16 * SR); t = np.arange(n) / SR; u = t / 0.16
        f = (330 + 620 * u ** 0.7) if kind == 'bubble' else (560 + 980 * u ** 0.7)
        return 0.26 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * np.clip(u, 0, 1)) ** 0.8
    raise KeyError(kind)


def music(dur, drums_from=0.0, mel_from=0.0):
    """Warm lo-fi bed: Cmaj7 - Am7 - Fmaj7 - G6, 84 bpm. Pad + bass + soft pluck arp + gentle kick/hat."""
    n = int(dur * SR) + SR
    out = np.zeros(n, np.float32)
    bpm = [84, 92, 78, 88, 82, 96][MUSIC_VARIANT % 6]; beat = 60 / bpm; bar = 4 * beat
    note = lambda m: 440 * 2 ** ((m - 69) / 12)
    CH = [[(48, [60, 64, 67, 71]), (45, [57, 60, 64, 67]), (53, [60, 65, 69, 72]), (55, [59, 62, 67, 71])],
          [(45, [57, 60, 64, 67]), (41, [57, 60, 65, 69]), (48, [60, 64, 67, 71]), (43, [59, 62, 67, 71])],
          [(50, [57, 60, 62, 65]), (43, [59, 62, 65, 67]), (48, [60, 64, 67, 71]), (45, [57, 60, 64, 67])],
          [(53, [60, 65, 69, 72]), (55, [59, 62, 67, 71]), (45, [57, 60, 64, 67]), (50, [57, 60, 62, 65])],
          [(48, [60, 64, 67, 71]), (43, [59, 62, 67, 71]), (45, [57, 60, 64, 67]), (53, [60, 65, 69, 72])],
          [(45, [57, 60, 64, 67]), (50, [57, 60, 62, 65]), (53, [60, 65, 69, 72]), (55, [59, 62, 67, 71])]]
    chords = CH[MUSIC_VARIANT % 6]
    nb = int(dur / bar) + 2
    rng = np.random.default_rng(5)
    for bi in range(nb):
        root, tones = chords[bi % 4]
        s0 = int(bi * bar * SR)
        L = int(bar * 1.15 * SR)
        t = np.arange(L) / SR
        env = np.minimum(1, t / 0.5) * np.minimum(1, (bar * 1.15 - t) / 0.7)
        pad = np.zeros(L)
        for m in tones:
            for det in (-0.004, 0.004):
                f = note(m) * (1 + det)
                pad += np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2 * f * t)
        pad *= env * 0.045
        # bass
        bass = np.zeros(L)
        for bt in (0, 2):
            ss = int(bt * beat * SR)
            tt = np.arange(L - ss) / SR
            bass[ss:] += np.sin(2 * np.pi * note(root - 12) * tt) * np.exp(-tt * 2.2) * 0.16
        # pluck arp (8ths)
        arp = np.zeros(L)
        seq = [tones[0], tones[1], tones[2], tones[3], tones[2], tones[1], tones[2], tones[3]]
        for k, m in enumerate(seq):
            ss = int(k * beat / 2 * SR)
            if ss >= L:
                break
            tt = np.arange(L - ss) / SR
            f = note(m + 12)
            arp[ss:] += (np.sin(2 * np.pi * f * tt) + 0.25 * np.sin(2 * np.pi * 2 * f * tt)) * np.exp(-tt * 9) * 0.05
        seg = pad + bass + arp
        if bi * bar >= mel_from:
            if MUSIC_VARIANT % 6 == 0:
                motifs = {0: [(0, 79), (3, 76), (4, 74), (6, 76)], 1: [(0, 76), (3, 72), (4, 74), (6, 72)],
                          2: [(0, 77), (3, 81), (4, 79), (6, 77)], 3: [(0, 79), (3, 74), (4, 71), (6, 74)]}[bi % 4]
            else:
                tn = [m + 12 if m < 64 else m for m in tones]
                motifs = [(0, tn[2]), (3, tn[1]), (4, tn[3] if bi % 2 else tn[0]), (6, tn[1])]
            mel = np.zeros(L)
            for step, m in motifs:
                ss = int(step * beat / 2 * SR)
                tt = np.arange(L - ss) / SR
                f = note(m)
                mel[ss:] += (np.sin(2 * np.pi * f * tt) + 0.35 * np.sin(2 * np.pi * 2 * f * tt) + 0.12 * np.sin(2 * np.pi * 3 * f * tt)) * np.exp(-tt * 5.5) * 0.06
            for sb in (1.5, 3.5):
                ss = int(sb * beat * SR)
                tt = np.arange(L - ss) / SR
                for m in tones[:3]:
                    f = note(m)
                    mel[ss:] += (np.sin(2 * np.pi * f * tt) + 0.5 * np.sin(2 * np.pi * 2 * f * tt)) * np.exp(-tt * 7) * 0.022
            seg = seg + mel
        out[s0:s0 + L] += seg[:max(0, min(L, n - s0))].astype(np.float32)[:len(out[s0:s0 + L])]
        # drums
        for bt in (range(4) if bi * bar >= drums_from else []):
            ss = s0 + int(bt * beat * SR)
            if bt in (0, 2):
                k = int(0.18 * SR); tt = np.arange(k) / SR
                kick = np.sin(2 * np.pi * np.cumsum(120 * np.exp(-tt * 28) + 42) / SR) * np.exp(-tt * 16) * 0.28
                out[ss:ss + k] += kick[:max(0, min(k, n - ss))].astype(np.float32)[:len(out[ss:ss + k])]
            else:
                k = int(0.12 * SR); tt = np.arange(k) / SR
                sn = rng.standard_normal(k) * np.exp(-tt * 28) * 0.06
                out[ss:ss + k] += sn[:max(0, min(k, n - ss))].astype(np.float32)[:len(out[ss:ss + k])]
        for h in (range(8) if bi * bar >= drums_from else []):
            ss = s0 + int((h * beat / 2 + (beat / 4 if False else 0)) * SR)
            k = int(0.03 * SR)
            hh = rng.standard_normal(k) * np.exp(-np.arange(k) / (0.008 * SR)) * (0.035 if h % 2 else 0.02)
            out[ss:ss + k] += hh[:max(0, min(k, n - ss))].astype(np.float32)[:len(out[ss:ss + k])]
    b, a = butter(2, 5200 / (SR / 2), 'low')
    out = lfilter(b, a, out).astype(np.float32)
    # slow tape-ish wobble-free; return
    return out[:int(dur * SR)]


# ------------------------------------------------------------------ timeline + audio
def build_timeline():
    from scenes import SCRIPT, events
    tl = []
    cur = 0.0
    narr_events = []   # (global_t, samples)
    caps = []
    sfx_ev = []
    for si, (sid, segs) in enumerate(SCRIPT):
        S = {}
        lead = 0.9 if si == 0 else 0.5
        t = lead
        clips = []
        for (k, say, show) in segs:
            x = tts(say, k)
            d = len(x) / SR
            S[k] = (t, d)
            clips.append((k, t, x, show or say))
            t += d + 0.26
        dur = t - 0.26 + (0.9 if si < len(SCRIPT) - 1 else 2.2)
        # extra breathing room for chart-heavy scenes
        if sid == 'savings':
            dur += 0.6
        tl.append(dict(sid=sid, start=cur, dur=dur, S=S))
        for k, ts, x, show in clips:
            narr_events.append((cur + ts, x))
            caps.append((cur + ts, cur + ts + len(x) / SR, show))
        for et, kind in events(sid, S):
            sfx_ev.append((cur + et, kind))
        if si < len(SCRIPT) - 1:
            sfx_ev.append((cur + dur - XF * 0.85, TRANS_SFX[TRANS[si % len(TRANS)]]))
        cur += dur
    total = cur
    return tl, total, narr_events, caps, sfx_ev


def split_caption(txt, maxc=44):
    import re
    parts = re.split(r'(?<=[.!?:])\s+', txt)
    out = []
    for p in parts:
        if len(p) <= maxc:
            out.append(p); continue
        sub = re.split(r'(?<=,)\s+', p)
        buf = ''
        for s in sub:
            if buf and len(buf) + len(s) + 1 > maxc:
                out.append(buf); buf = s
            else:
                buf = (buf + ' ' + s).strip()
        if buf:
            out.append(buf)
    final = []
    for p in out:
        if len(p) <= maxc + 8:
            final.append(p); continue
        words = p.split(); buf = ''
        # balance into near-equal chunks
        nchunks = math.ceil(len(p) / maxc)
        target = len(p) / nchunks
        for w in words:
            if buf and len(buf) + len(w) + 1 > target + 6:
                final.append(buf); buf = w
            else:
                buf = (buf + ' ' + w).strip()
        if buf:
            final.append(buf)
    return final


def cap_chunks(caps):
    chunks = []
    for t0, t1, txt in caps:
        parts = split_caption(txt)
        tot = sum(len(p) for p in parts)
        t = t0
        for p in parts:
            d = (t1 - t0) * len(p) / tot
            chunks.append((t, t + d, p))
            t += d
    return chunks


def srt_time(x):
    h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60
    return f'{h:02d}:{m:02d}:{int(s):02d},{int((s - int(s)) * 1000):03d}'


def do_audio():
    tl, total, narr, caps, sfx_ev = build_timeline()
    n = int((total + 1) * SR)
    voice = np.zeros(n, np.float32)
    for t0, x in narr:
        i = int(t0 * SR)
        voice[i:i + len(x)] += x
    ts = [x['start'] for x in tl if x['sid'] == 'title'][0]
    mus = music(total + 1, drums_from=ts, mel_from=ts)
    sfx_ev += [(ts + 0.1, 'sting'), (ts - 2.3, 'riser')]
    # duck music under voice
    env = np.abs(voice)
    k = int(0.25 * SR)
    env = np.convolve(env, np.ones(k) / k, 'same')
    env = np.clip(env / 0.08, 0, 1)
    k2 = int(0.35 * SR)
    env = np.convolve(env, np.ones(k2) / k2, 'same')
    gain = 1.0 - 0.62 * env
    mus = mus * gain.astype(np.float32)
    # fade in / out
    fi = int(1.5 * SR); mus[:fi] *= np.linspace(0, 1, fi)
    fo = int(3.0 * SR); mus[int(total * SR) - fo:int(total * SR)] *= np.linspace(1, 0, fo); mus[int(total * SR):] = 0
    mix = voice * 1.0 + mus * 0.85
    for t0, kind in sfx_ev:
        x = sfx(kind)
        i = int(t0 * SR)
        if i < 0 or i + len(x) > n:
            continue
        mix[i:i + len(x)] += x.astype(np.float32)
    mix = np.tanh(mix * 0.9) / 0.9 * 0.9
    wavfile.write(f'{WORK}/mix_raw.wav', SR, (np.clip(mix, -1, 1) * 32767).astype(np.int16))
    sh(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{WORK}/mix_raw.wav', '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11', '-ar', '44100', '-ac', '2', f'{WORK}/mix.wav'])
    chunks = cap_chunks(caps)
    PUNCH = {'thud', 'cash', 'coin', 'coin2', 'boom', 'sting', 'sparkle'}
    pulses = sorted(t for t, k in sfx_ev if k in PUNCH)
    json.dump(dict(tl=tl, total=total, caps=chunks, pulses=pulses, trans=[TRANS[i % len(TRANS)] for i in range(len(tl))]), open(f'{WORK}/timeline.json', 'w'))
    with open(f'{OUT}/captions.srt', 'w') as f:
        for i, (a, b, txt) in enumerate(chunks, 1):
            f.write(f'{i}\n{srt_time(a)} --> {srt_time(b)}\n{txt}\n\n')
    print(f'total {total:.1f}s = {int(total // 60)}:{int(total % 60):02d}; scenes:')
    for s in tl:
        print(f"  {s['sid']:9s} start {s['start']:6.1f} dur {s['dur']:5.1f}")
    words = sum(len(say.split()) for _, segs in __import__('scenes').SCRIPT for _, say, _ in segs)
    print('words', words)


# ------------------------------------------------------------------ rendering
_T = None


def load():
    global _T
    if _T is None:
        _T = json.load(open(f'{WORK}/timeline.json'))
    return _T


def zoom_img(im, z):
    from PIL import Image
    if z <= 1.0005:
        return im
    w_, h_ = im.size
    cw, ch = w_ / z, h_ / z
    x0, y0 = (w_ - cw) / 2, (h_ - ch) / 2
    return im.resize((w_, h_), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch))


def scene_frame(idx, t, T):
    from PIL import Image
    from lib import W, H, clamp
    import scenes
    s = T['tl'][idx]
    S = {k: tuple(v) for k, v in s['S'].items()}
    lt = t - s['start']
    img = Image.new('RGBA', (W, H), (0, 0, 0, 255))
    scenes.RENDER[s['sid']](img, lt, S)
    z = 1 + 0.05 * clamp(lt / s['dur'])                    # slow push-in
    for te in T['pulses']:                                   # beat "punch" on impactful sounds
        dt = t - te
        if 0 <= dt < 0.7:
            z += 0.022 * math.exp(-dt / 0.13)
    return zoom_img(img, z)


def transition(a, b, p, kind):
    from PIL import Image
    from lib import W, H, e_inout, e_out, clamp
    import numpy as _np
    if kind == 'slide':
        off = int(W * e_inout(p))
        c = Image.new('RGBA', (W, H), (0, 0, 0, 255)); c.paste(a, (-off, 0)); c.paste(b, (W - off, 0)); return c
    if kind == 'zoom':
        q = e_inout(p)
        a2 = zoom_img(a, 1 + 0.55 * q); b2 = zoom_img(b, 1.45 - 0.45 * q)
        return Image.blend(a2, b2, clamp(q * 1.15 - 0.1))
    if kind == 'wipe':
        gw, gh = 96, 54
        xs = _np.linspace(0, 1, gw)[None, :]; ys = _np.linspace(0, 1, gh)[:, None]
        u = xs * 0.85 + ys * 0.15
        m = _np.clip((e_inout(p) * 1.18 - u) / 0.18, 0, 1)
        mask = Image.fromarray((m * 255).astype(_np.uint8), 'L').resize((W, H), Image.BILINEAR)
        return Image.composite(b, a, mask)
    if kind == 'flash':
        white = Image.new('RGBA', (W, H), (255, 255, 255, 255))
        return Image.blend(a, white, e_out(p * 2) * 0.95) if p < 0.5 else Image.blend(white, b, e_out((p - 0.5) * 2))
    return Image.blend(a, b, e_inout(p))


def render_frame(i):
    from PIL import Image, ImageDraw
    from lib import W, H, FPS, e_inout, logo_chip, text, text_w, Cv, rgba, WHITE, clamp
    T = load()
    t = i / FPS
    tl = T['tl']
    k = 0
    for j, s in enumerate(tl):
        if s['start'] <= t:
            k = j
    end = tl[k]['start'] + tl[k]['dur']
    img = scene_frame(k, t, T)
    if k + 1 < len(tl) and t > end - XF:
        img2 = scene_frame(k + 1, t, T)
        img = transition(img, img2, clamp((t - (end - XF)) / XF), T['trans'][k])
    s = tl[k]
    if s['sid'] not in ('title',):
        logo_chip(img, 0.95)
    tot = T['total']
    d = ImageDraw.Draw(img, 'RGBA')
    d.rectangle([0, H - 7, W, H], fill=(255, 255, 255, 30))
    d.rectangle([0, H - 7, int(W * t / tot), H], fill=(25, 195, 125, 255))
    for a, b, txt in T['caps']:
        if a - 0.05 <= t <= b + 0.15:
            fade = clamp((t - (a - 0.05)) / 0.18)
            tw = text_w(txt, 40, 'Bold')
            box = (W / 2 - tw / 2 - 34, 996, W / 2 + tw / 2 + 34, 1060)
            cv = Cv((box[0] - 3, box[1] - 3, box[2] + 3, box[3] + 3))
            cv.rrect(box, 32, fill=rgba((6, 14, 30), 205))
            cv.paste(img, fade)
            text(img, (W / 2, 1028), txt, 40, 'Bold', WHITE, 'mm', fade)
            break
    return img.convert('RGB')


def worker(args):
    f0, f1, idx = args
    out = f'{WORK}/chunk_{idx:02d}.mp4'
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1920x1080', '-r', '30', '-i', '-',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', '-pix_fmt', 'yuv420p', '-g', '60', out], stdin=subprocess.PIPE)
    for i in range(f0, f1):
        p.stdin.write(render_frame(i).tobytes())
    p.stdin.close(); p.wait()
    return out


def do_render():
    from multiprocessing import Pool
    T = load()
    nf = int(math.ceil(T['total'] * 30))
    nproc = 4
    per = 240
    jobs = [(f, min(nf, f + per), j) for j, f in enumerate(range(0, nf, per))]
    print('frames', nf, 'chunks', len(jobs), flush=True)
    with Pool(nproc) as pool:
        for k, o in enumerate(pool.imap(worker, jobs)):
            print('done', k + 1, '/', len(jobs), flush=True)
    with open(f'{WORK}/list.txt', 'w') as f:
        for j in range(len(jobs)):
            f.write(f"file 'chunk_{j:02d}.mp4'\n")
    sh(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'{WORK}/list.txt', '-c', 'copy', f'{WORK}/video_silent.mp4'])
    final = f'{OUT}/{FINAL_NAME}'
    sh(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{WORK}/video_silent.mp4', '-i', f'{WORK}/mix.wav', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
        '-shortest', '-movflags', '+faststart', final])
    print('wrote', final)


if __name__ == '__main__':
    import lib
    lib.SPEED = float(os.environ.get('B2B_GFX_SPEED', '1.7'))
    lib.BG = float(os.environ.get('B2B_BG_SPEED', '2.2'))
    cmd = sys.argv[1]
    if cmd == 'audio':
        do_audio()
    elif cmd == 'preview':
        os.makedirs(f'{WORK}/prev', exist_ok=True)
        for tt in sys.argv[2:]:
            render_frame(int(float(tt) * 30)).save(f'{WORK}/prev/f_{float(tt):06.1f}.png')
            print('saved', tt)
    elif cmd == 'render':
        do_render()
