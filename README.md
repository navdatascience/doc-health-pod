# Doctor Health Podcast Library

Full transcripts + analyzed key tidbits from health and doctor podcasts, collected as one markdown file per episode.

**Started:** 2026-11-18 · **Updated weekly** — every week all three sources are re-audited for new health episodes, the backlog is processed in batches, and new files are pushed here.

## Sources

| Source | What is included | Channel / playlist |
|---|---|---|
| Dr Pal Podcast Playlist | **All** episodes in the playlist | https://www.youtube.com/playlist?list=PLVlf929ZD8laSTsczo4BlVS_NS4vBMS19 |
| Raj Shamani (Figuring Out) | **Health-only** episodes (doctor guests, medical, nutrition, sleep, mental-health topics) | https://www.youtube.com/@rajshamani/videos |
| The Diary Of A CEO | **Health-only** episodes (doctor/scientist guests, medical, longevity, brain, gut, sleep topics) | https://www.youtube.com/@TheDiaryOfACEO/videos |

Excluded from Raj Shamani / DOAC: business, geopolitics, celebrity and dating interviews where health is not the topic, even if a title mentions a doctor, psychology, trauma or heartbreak in passing. The full audited inventory with per-episode status lives in `catalog.json` and `INDEX.md`.

## Layout

- `episodes/dr-pal/` — Dr Pal playlist episodes
- `episodes/raj-shamani/` — Raj Shamani health episodes
- `episodes/diary-of-a-ceo/` — Diary Of A CEO health episodes
- `catalog.json` — machine-readable inventory (372 episodes at launch) with `pending` / `done` status per episode
- `INDEX.md` — human-readable index, regenerated on every push
- `scripts/fetch_transcript.py` — transcript fetcher (youtube-transcript-api; pace requests, YouTube throttles bursts)

## Episode file format

Each episode markdown contains: source, guest, YouTube link, **Important tidbits** (specific takeaways, numbers and protocols actually stated), **Claims to be careful with**, a short summary, and the **full transcript**.

> Transcripts are YouTube captions for personal study. Tidbits summarize what the guest said — they are not medical advice.
