#!/usr/bin/env python3
"""Fetch a YouTube transcript with youtube-transcript-api and save clean text.
Usage: fetch_transcript.py <video_id> <out_path>
Tries en, then en-IN/en-GB/en-US, then any available transcript (translated to en if needed).
Prints char/word counts on success."""
import sys, time
from youtube_transcript_api import YouTubeTranscriptApi

def main():
    vid, out = sys.argv[1], sys.argv[2]
    ytt = YouTubeTranscriptApi()
    last = None
    for attempt in range(3):
        try:
            t = ytt.fetch(vid, languages=['en', 'en-IN', 'en-GB', 'en-US'])
            text = ' '.join(s.text.replace('\n', ' ') for s in t)
            break
        except Exception as e:
            last = e
            try:
                tl = ytt.list(vid)
                tr = next(iter(tl))
                t = tr.fetch()
                text = ' '.join(s.text.replace('\n', ' ') for s in t)
                break
            except Exception as e2:
                last = e2
                time.sleep(5 * (attempt + 1))
    else:
        print(f"FAIL {vid}: {type(last).__name__} {last}")
        sys.exit(1)
    with open(out, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"OK {vid}: {len(text)} chars, {len(text.split())} words -> {out}")

if __name__ == '__main__':
    main()
