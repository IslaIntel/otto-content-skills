---
name: reel-script
description: Write a full short-video script beat by beat (spoken line, on-screen text for sound-off viewers, visual and timing for each beat, plus the caption handoff), sized to how long your viewers actually watch, using average watch time pulled through the Otto MCP. Use when someone says "script this reel", "write the video", "turn this idea into a reel", "what do I say in this video", "write the on-screen text", or "make this shorter".
license: MIT
---

# Reel script

Produces a script you can film from: every beat has what you say, what's written on screen, what the camera sees, and how long it lasts. Its length is set from your own viewers' average watch time, not a generic "30 to 45 seconds".

Read-only on every platform. Next steps: `shot-list` (what to film), `cover-designer`, `caption-writer`, `sound-human` (final voice pass).

## 1. Setup
Follow the settings, scope and capability rules in `otto-rules.md` (in this skill's folder) ("How every skill talks to the user"). In short: read `brand/settings.md` (or memory) for workspace, Instagram / YouTube accounts and output mode; ask only what's missing in one multiple-choice message and save it. Output is visual by default (artifact / HTML file / canvas) unless settings say chat.

- Read `brand/` (voice, audience, offer, facts, winners). Missing: ask what you sell, who it's for, the one action, how you sound. Suggest `brand-brain`.
- Inputs: the idea or the plan from `viral-reel-planner`, the chosen hook (or run `hook-writer`), the goal, and whether the owner talks on camera, does voiceover, or shows text only.

## 2. Pull: how long do your viewers stay?
- `meta_ig_list_media` (rowLimit 60) and `meta_ig_media_insights` (batches of 25): `reach, ig_reels_avg_watch_time, reels_skip_rate, shares, saved`. Reels at least 3 days old. Request `ig_reels_avg_watch_time` and `reels_skip_rate` only for `mediaType: VIDEO` ids (one image in the batch fails the whole call).
- Get each reel's length from the `efg` value in its `mediaUrl` (decode it with code, see `otto-rules.md`); where `mediaUrl` is null, ask the length of your best 5 reels. With length, compute watch % = avg watch seconds / length.
- YouTube Shorts: `youtube_top_videos` gives `averageViewDuration` in seconds. It doesn't mark which videos are Shorts: pick them by length or ask.

`ig_reels_avg_watch_time` is **milliseconds**: divide by 1,000.

**Length target**

| Your data | Target length |
|---|---|
| Median watch % above 70% | median avg watch seconds x 1.4 (room to grow) |
| 40 to 70% | median avg watch seconds x 1.2 |
| Below 40% | median avg watch seconds + 2s; fix holding before adding length |
| Lengths unknown | median avg watch seconds of your best reels in this format x 1.2; say the target is an estimate |
| No data | 15 to 25s, labelled "no baseline yet" |

If the format needs more (a tutorial with 5 steps), say so and add a turn every 4 to 6 seconds to earn it.

Not connected or `ok: false`: use the "no data" row and say why.

## 3. Write the beats

Speaking pace: about 2.5 words per second for a normal talker. Count words per beat and check the timing adds up to the target.

| Beat | Job | Rule |
|---|---|---|
| 1. Hook (0 to ~2s) | stop the scroll | the chosen hook; first word within 0.5s |
| 2. Stakes (~2 to 5s) | why this matters to the viewer | their words from `brand/audience.md` |
| 3+. Body | deliver, one idea per beat | each beat changes the picture; one new fact, step or turn |
| Payoff | pay the hook's promise | shown, not only said |
| CTA (last 2 to 3s) | one action | matches the goal; same keyword as the caption |

For every beat write:
- **Spoken**: the exact words, in the owner's voice.
- **On-screen text**: the headline of the beat in 7 words or fewer, not a transcript. Mark the one word to emphasise in **bold**. It appears on the spoken word it matches.
- **Visual**: what the camera sees. If two beats in a row show the same picture, change one.
- **Time**: start and end seconds.

**Mute test**: read only the on-screen text column top to bottom. If the story is lost with the sound off, rewrite the lines that carry it and say which.

**Safe area**: keep text out of the top 14% and bottom 35% of a 9:16 frame, and about 6% in from each side (the buttons sit on the right). This is the common guideline from Meta's ad specs; Instagram publishes no exact numbers for regular Reels, so it errs on the safe side.

## 4. Pre-flight checklist (all must pass)

- [ ] Hook passes `hook-writer`'s checks; first word under 0.5s.
- [ ] Every number appears in `brand/facts.md` or the pull.
- [ ] The payoff delivers what the hook promised.
- [ ] Total length within 2s of the target; word count fits the pace.
- [ ] Mute test passes.
- [ ] One CTA only; if it's a comment keyword, the DM content exists (`comment-to-lead`).
- [ ] No beat over 6 seconds without a visual change.
- [ ] Read aloud once at normal speed. Anything you stumble on gets rewritten (`sound-human`).
- [ ] Audio: original or licensed. Trending sounds on a business account may be restricted; say so.

## 5. Output

Default is visual (artifact / HTML file / canvas); chat if settings or the user say so.

```
SCRIPT: <title> | goal: <goal> | target <s>s (your median watch <s>s, <n> reels)
Format: <talking head / voiceover / text-only>

| # | Time | Spoken | On-screen text | Visual |
|---|---|---|---|---|
| 1 | 0.0-1.8 | "..." | "...**word**..." | ... |
...
Word count: <n> (~<s>s at 2.5 w/s)

Mute read: <the on-screen lines in order>
Pre-flight: <passed / which failed and the fix>

Caption handoff -> caption-writer:
  First line: <hook restated for the feed>
  Keyword/CTA: <same as last beat>
  Depth to move into the caption: <what was cut from the reel>
```

## Never
- Pad to reach a length. Short and finished beats long and saggy.
- Put a claim on screen that `brand/facts.md` lists as not allowed.
- Script someone else's footage or voice without their permission.
