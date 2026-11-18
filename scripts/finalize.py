#!/usr/bin/env python3
"""Append cached transcripts to any episode .md still carrying the
TRANSCRIPT_BELOW marker, mark those episodes done in catalog.json,
and regenerate INDEX.md. Safe to run repeatedly (per wave)."""
import json, pathlib, sys, datetime
REPO = pathlib.Path('/home/hatch/workspace/doc-health-pod-repo')
cat = json.load(open(REPO / 'catalog.json'))
today = datetime.date.today().isoformat()
done_now = []
for e in cat['episodes']:
    if e['status'] == 'done':
        continue
    md = REPO / e['file']
    cache = REPO / 'transcripts-cache' / f"{e['id']}.txt"
    if md.exists() and cache.exists() and cache.stat().st_size > 500:
        content = md.read_text(encoding='utf-8')
        if '<!-- TRANSCRIPT_BELOW -->' in content:
            transcript = cache.read_text(encoding='utf-8').strip()
            md.write_text(content.replace('<!-- TRANSCRIPT_BELOW -->', transcript), encoding='utf-8')
            e['status'] = 'done'
            e['collected'] = today
            done_now.append(e['id'])
json.dump(cat, open(REPO / 'catalog.json', 'w'), indent=2)
done = [e for e in cat['episodes'] if e['status'] == 'done']
lines = ["# Index — Doctor Health Podcast Library", "",
         f"**{len(done)} of {cat['total']} episodes collected** · Updated {today}", "",
         f"- Dr Pal Podcast Playlist: {sum(1 for e in cat['episodes'] if e['source']=='dr-pal' and e['status']=='done')} / {cat['counts']['dr-pal']} done",
         f"- Raj Shamani (health): {sum(1 for e in cat['episodes'] if e['source']=='raj-shamani' and e['status']=='done')} / {cat['counts']['raj-shamani']} done",
         f"- The Diary Of A CEO (health): {sum(1 for e in cat['episodes'] if e['source']=='diary-of-a-ceo' and e['status']=='done')} / {cat['counts']['diary-of-a-ceo']} done", ""]
for src, name in [("dr-pal", "Dr Pal Podcast Playlist"), ("raj-shamani", "Raj Shamani — health episodes"), ("diary-of-a-ceo", "The Diary Of A CEO — health episodes")]:
    lines += [f"## {name}", ""]
    for e in [x for x in cat['episodes'] if x['source'] == src]:
        if e['status'] == 'done':
            lines.append(f"- ✅ [{e['title']}]({e['file']}) — [YouTube]({e['url']})")
        else:
            lines.append(f"- ⏳ {e['title']} — [YouTube]({e['url']})")
    lines.append("")
(REPO / 'INDEX.md').write_text("\n".join(lines), encoding='utf-8')
print(f"finalized this run: {done_now}")
print(f"total done: {len(done)} of {cat['total']}")
