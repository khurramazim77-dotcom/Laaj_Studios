#!/usr/bin/env python3
"""Search Pixabay's video API (official, with your own API key) and download candidate clips via curl.
PIXABAY_KEY must be in the environment (never stored in files).
usage: python fetch_footage.py CLIPDIR name "query" [name "query" ...]  -> CLIPDIR/<name>_<n>.mp4 + credits in ../footage/credits.json"""
import os, sys, json, subprocess, urllib.parse
key = os.environ['PIXABAY_KEY']
clipdir = sys.argv[1]; os.makedirs(clipdir, exist_ok=True)
credits_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'footage', 'credits.json')
credits = json.load(open(credits_path)) if os.path.exists(credits_path) else {}
args = sys.argv[2:]
for name, q in zip(args[::2], args[1::2]):
    url = 'https://pixabay.com/api/videos/?' + urllib.parse.urlencode(dict(key=key, q=q, per_page=20, safesearch='true', video_type='film'))
    r = subprocess.run(['curl', '-s', '-m', '40', url], capture_output=True, text=True)
    try:
        hits = json.loads(r.stdout)['hits']
    except Exception:
        print('API error for', q, r.stdout[:120]); continue
    hits = [h for h in hits if h['duration'] >= 8 and h['videos']['medium']['width'] >= 1280][:3]
    for n, h in enumerate(hits):
        v = h['videos']['medium']; out = f'{clipdir}/{name}_{n}.mp4'
        if not os.path.exists(out):
            subprocess.run(['curl', '-s', '-m', '120', '-o', out, v['url']])
        ok = os.path.exists(out) and os.path.getsize(out) > 50000
        credits[f'{name}_{n}'] = dict(pixabay_id=h['id'], page=h['pageURL'], user=h['user'], query=q, duration=h['duration'], size=f"{v['width']}x{v['height']}")
        print(name, n, h['id'], h['duration'], f"{v['width']}x{v['height']}", 'OK' if ok else 'DOWNLOAD FAILED', h['tags'][:40], flush=True)
json.dump(credits, open(credits_path, 'w'), indent=1)
