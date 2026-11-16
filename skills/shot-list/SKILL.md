---
name: shot-list
description: Turn a reel script into a phone-only shot list for filming real footage, in filming order, grouped by location, with framing, duration and the line each shot covers, and check your Otto media library for footage you already have. Use when someone says "shot list for this script", "what should I film for this", "plan my B-roll", or "plan my filming day".
license: MIT
---

# Shot list

A shot list for filming real footage: everything to film for one script (or a batch of scripts), in the order you'd actually shoot it. All the shots in one place before you move; the hardest-to-repeat moments first. Built for one person with a phone.

Read-only. It lists footage in the Otto library; it never uploads, generates or deletes anything. Every shot is real footage you film yourself; nothing here is generated.

## 1. Setup
Follow the settings, scope and capability rules in `otto-rules.md` (in this skill's folder) ("How every skill talks to the user"). In short: read `brand/settings.md` (or memory) for workspace, accounts and output mode; ask only what's missing in one multiple-choice message and save it. Output is visual by default (artifact / HTML file / canvas) unless settings say chat.

- Input: a script from `reel-script` (or any script with beats). No script? Run `reel-script` first.
- Ask: where can you film (shop, kitchen, car, client site, desk)? Who can be on camera? Any time limit? Is it vertical only (9:16) or also needed in 16:9 for YouTube?
- Read `brand/offer.md` to know which products or services must look right on camera.

## 2. Check what you already have
- `media_list` (kind `video`, limit 100, then kind `image`) lists the Otto library: filename, kind, createdAt. Match filenames to beats ("storefront", "before", "product") and ask the owner to confirm a clip is usable before you drop a shot.
- `meta_ig_list_media` (rowLimit 50): earlier reels can't be reused as raw footage, but their `mediaUrl` (when not null) lets the owner rewatch a shot they liked and reproduce it.
- `ok: false` or nothing relevant: plan to film everything.

## 3. Build the list

1. **One shot per visual change in the script.** A shot that doesn't cover a line is cut, and you say so.
2. **Group by location**, then by setup (same angle and light) inside each location.
3. **Order** inside a location: shots that need people or perishable things first (food, a customer, daylight), close-ups last.
4. **For each shot** write: number, location, the script beat it covers, what's in frame, framing, camera move, how long to roll, and essential or nice-to-have.
5. **Two formats**: if 16:9 is also needed, frame wide with the subject in the centre so both crops work.
6. **Roll long**: film at least 2 seconds before and after the action you need, and 3 takes of anything with a spoken line.
7. **Hook shot**: mark the beat-1 shot and film 2 versions (different first frame) so `hook-test` can compare them later.

Framing words to use: wide (whole scene), medium (waist up or the full counter), close (hands, product), detail (a label, a screen, a number), over-the-shoulder, top-down.

## 4. Phone-only tips (include the ones that apply)

| Situation | Tip |
|---|---|
| Talking to camera | Lens at eye level, phone 50 to 70cm away, window in front of you not behind. Use the back camera with a mirror or a friend if you can; it's sharper |
| Sound | Film 1m or closer to the speaker; a quiet room beats any filter. Record a 10s silence for clean-up |
| Movement | Hold with two hands, elbows in; walk heel-to-toe. Slow pans only |
| Screens | Record the screen with the phone's built-in recorder instead of filming the monitor |
| Product | A white sheet of paper as a bounce under the product; turn off overhead lights that cast hard shadows |
| Exposure | Tap and hold to lock focus and exposure before rolling |
| Settings | 1080p or 4K, 30fps; 60fps only for slow motion. Lens clean. Airplane mode |
| Safe zone | Keep faces and text out of the top 14% and bottom 35% of the frame (Reels) |

## 5. Output

Default is visual (artifact / HTML file / canvas); chat if settings or the user say so.

```
SHOT LIST: <reel title> | <n> shots | ~<minutes> of filming
Already in your Otto library: <filenames that cover which beats, or "none matched">

LOCATION 1: <place> (film first because <reason>)
| # | Beat | In frame | Framing / move | Roll | Priority |
|---|---|---|---|---|---|
| 1 | Hook (A) | ... | close, static, top-down | 6s, 3 takes | essential |
| 2 | Hook (B) | ... | medium, push in | 6s, 3 takes | essential |
...

LOCATION 2: ...

If time runs out, drop: #<n>, #<n> (nice-to-have)
Can't film it? Use a still or screen recording instead: <shot and alternative>
Kit: phone, <only what this list needs>
```

## Never
- Add shots that don't cover a line.
- Suggest filming customers, staff or private screens without their OK.
- Recommend another creator's footage.
