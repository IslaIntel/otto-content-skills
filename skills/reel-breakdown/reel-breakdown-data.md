# Filling reel-breakdown.html

`reel-breakdown.html` (next to this file) is the finished design. To show a breakdown:

1. Copy it. Replace **only** the JSON inside `<script id="otto-data" type="application/json">`. Don't edit the HTML: the tab title comes from `meta.title`. Keep the Otto mark.
2. Leave out what you don't have; every section hides itself when its data is missing.
3. Show it as an artifact (claude.ai / Claude desktop), save and open it as `social-data/reports/breakdown-<slug>.html` (Claude Code / Cowork), or a canvas (ChatGPT). Chat mode: give the same content as text instead.

**Frames.** One frame per shot (from the middle of the shot) and the hook frames at 0, 0.5, 1, 2 and 3 s, as JPEG data URIs: about 200 px wide for shots, 240 px for hook frames, quality around 75 (ffmpeg `-vf scale=200:-2 -q:v 6`). Keep the whole file under ~1 MB; with 20+ shots, drop to 160 px. No frames available (screenshots only): use the screenshots as hook frames and leave `frame` off the shots; the timeline still shows the text.

**Write the verdict last**, from the numbers on the page.

```json
{
  "meta": {
    "title": "the reel's hook line or title",
    "series": "After Hours, ep 31",            // optional
    "length_s": 21.7, "posted": "Nov 12, 2026",
    "permalink": "https://www.instagram.com/reel/…/",
    "accounts": [{"platform": "instagram", "handle": "@bloomandstem", "url": "https://www.instagram.com/bloomandstem/"}],
    "source": "Supplied by you (someone else's reel)",   // instead of accounts, for other people's reels
    "baselineLabel": "your usual (last 28 days)",
    "generated": "Mar 10, 2026", "footnote": "Built from live Otto data",
    "verdict": "One or two sentences: how it did and where people left."
  },
  "kpis": [                                   // own reels only, 3-5 tiles (they sit in one row); a metric with no signal (shares at 0 everywhere) goes in notes, not a tile. Others' reels: what's visible on the post, with the date seen
    {"label": "Reach", "value": 1322, "baseline": 934},
    {"label": "Skip rate", "value": 26.2, "baseline": 31.5, "unit": "%", "lowerIsBetter": true},
    {"label": "Avg watch", "value": 12.0, "unit": " s", "baseline": 11.2, "vsLabel": "similar-length reels"}   // vsLabel: what this tile is compared with, when it differs from meta.baselineLabel
  ],
  "timeline": {
    "length_s": 21.7,
    "shots": [ {"start": 0, "end": 2.33, "frame": "data:image/jpeg;base64,…", "text": "on-screen text", "said": "spoken line", "note": "optional: who speaks, what changes"} ],   // no transcript: leave said off and put the speaker in note
    "sections": [ {"label": "Setup", "start": 0, "end": 2.33}, {"label": "Payoff", "start": 15.9, "end": 17.7} ],
    "markers": [                              // as many as needed. kind: leave (amber, avg watch point) | payoff (green; a reel can have two) | drop (red, a retention drop)
      {"t": 12.0, "label": "Avg viewer leaves · 12.0 s", "kind": "leave"},
      {"t": 15.9, "label": "Payoff · 15.9 s", "kind": "payoff"}
    ],
    "note": "One line under the timeline"
  },
  "hook": {
    "frames": [ {"t": 0, "frame": "data:image/jpeg;base64,…", "note": "what's on screen and said"} ],
    "checks": [ {"status": "pass", "label": "Readable with the sound off", "note": "why"} ]   // pass | fail | skip
  },
  "structure": [ {"beat": "Setup", "start": 0, "end": 2.33, "what": "what happens"} ],
  "pacing": {"note": "optional line; cuts, cuts per 10 s, longest and shortest shot are computed from the shots"},
  "onscreen": [ {"t": 0, "text": "…"} ],      // optional: defaults to each shot's text
  "cta": {"present": false, "text": "what the ask is, or what's missing", "note": "optional suggestion"},
  "finding": "The one thing the numbers and the timeline show together.",
  "change": "One change to try next, changing one thing only.",
  "borrow": ["what's worth copying (other people's reels: structure, never their words)"],
  "leave": ["what not to copy"],
  "notes": ["caveats: no audio transcript, baseline window, etc."]
}
```

Rules: the `//` comments are explanations only; the JSON in the file must not contain them. Numbers are numbers. Times are seconds from the start.
