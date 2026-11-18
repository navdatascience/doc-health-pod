#!/usr/bin/env python3
"""Fetch transcripts for ALL pending catalog episodes, resumable.
Skips episodes already in transcripts-cache/. Paces requests, retries once.
Writes progress to ~/workspace/doc-health-pod-work/fetch-all.log and a
status JSON it updates as it goes."""
import json, pathlib, sys, time
from youtube_transcript_api import YouTubeTranscriptApi

REPO = pathlib.Path('/home/hatch/workspace/doc-health-pod-repo')
LOG = pathlib.Path('/home/hatch/workspace/doc-health-pod-work/fetch-all.log')
STATUS = pathlib.Path('/home/hatch/workspace/doc-health-pod-work/fetch-status.json')

def log(msg):
    line = f"{time.strftime('%H:%M:%S')} {msg}"
    print(line, flush=True)
    with open(LOG, 'a') as f: f.write(line + '\n')

def fetch_one(ytt, vid):
    try:
        t = ytt.fetch(vid, languages=['en', 'en-IN', 'en-GB', 'en-US', 'hi'])
        return ' '.join(s.text.replace('\n', ' ') for s in t)
    except Exception:
        tl = ytt.list(vid)
        tracks = list(tl)
        # Prefer English, then Hindi, then any track translated to English.
        pref = None
        for tr in tracks:
            if tr.language_code.startswith('en'):
                pref = tr; break
        if pref is None:
            for tr in tracks:
                if tr.language_code.startswith('hi'):
                    pref = tr; break
        if pref is None:
            pref = tracks[0].translate('en')
        t = pref.fetch()
        return ' '.join(s.text.replace('\n', ' ') for s in t)

def main():
    cat = json.load(open(REPO / 'catalog.json'))
    pending = [e for e in cat['episodes'] if e['status'] != 'done']
    ytt = YouTubeTranscriptApi()
    ok, fail, skip = 0, 0, 0
    failures = []
    for i, e in enumerate(pending):
        vid = e['id']
        out = REPO / 'transcripts-cache' / f'{vid}.txt'
        if out.exists() and out.stat().st_size > 500:
            skip += 1
            continue
        done_attempt = False
        for attempt in range(2):
            try:
                text = fetch_one(ytt, vid)
                out.write_text(text, encoding='utf-8')
                ok += 1
                done_attempt = True
                log(f"[{i+1}/{len(pending)}] OK {vid} {len(text.split())}w {e['title'][:60]}")
                break
            except Exception as ex:
                if attempt == 0:
                    log(f"[{i+1}/{len(pending)}] retry {vid}: {type(ex).__name__}")
                    time.sleep(30)
                else:
                    fail += 1
                    failures.append({'id': vid, 'title': e['title'], 'error': type(ex).__name__})
                    log(f"[{i+1}/{len(pending)}] FAIL {vid}: {type(ex).__name__}")
        STATUS.write_text(json.dumps({'ok': ok, 'fail': fail, 'skip': skip, 'failures': failures}, indent=2))
        time.sleep(4)
    log(f"DONE ok={ok} fail={fail} skip={skip}")

if __name__ == '__main__':
    main()
