---
name: hook-patterns
description: Mine the hooks from your own posts (first caption line or first spoken line), rank them on the numbers Otto pulls from Instagram, Facebook, LinkedIn and YouTube (skip rate, watch time, shares per 1,000 reach), sort them into patterns, and remix the winners into new hooks that keep the structure and change the words. Optionally takes a CSV of other hooks. Use when asked to "mine my hooks", "which openings work for me", "remix my best hooks", "hook variations from what's working", or "give me hooks based on my data".
license: MIT
---

# Hook mining

Your best hooks already exist; they're sitting in your own feed with numbers attached. This skill finds them, works out which **pattern** they share, and writes new hooks on the same skeleton. It never invents hooks from nothing (that's `hook-writer`) and never reuses someone else's line word for word. Read-only on every platform.

## 0. Setup

Follow the settings, scope and capability rules in `otto-rules.md` (in this skill's folder) ("How every skill talks to the user"). In short:
- Read `brand/settings.md` (or your memory of the user's Otto settings) first: workspace, accounts, default platforms, timezone, output mode. Ask only what's missing, as one multiple-choice question, and save the answers.
- Scope is the platforms the user names; otherwise the default from settings; otherwise ask once, listing connected platforms plus "All connected". A platform in scope with nothing in the window gets one line, never an empty table.

Then:
- Read `brand/voice.md` (words to use and avoid) and `brand/winners.md` if they exist.
- Ask: is the first spoken line usually different from the first caption line? If yes, ask for the spoken lines of the top and bottom 10 reels (or a transcript). Without them, rank caption hooks only and say so.
- Optional: a CSV of other hooks (a competitor's, a swipe file). It's used only for pattern ideas, never ranked against your own numbers, and never copied.

## 1. Pull

- **Instagram**: `meta_ig_list_media` (rowLimit 60) for captions; `meta_ig_media_insights` in batches of 25: `views, reach, shares, saved, comments, ig_reels_avg_watch_time, reels_skip_rate`. Watch time is ms; skip rate is already a percent. Request `ig_reels_avg_watch_time` and `reels_skip_rate` only for `mediaType: VIDEO` ids (one image in the batch fails the whole call).
- **Facebook**: `meta_page_posts` (message) + `meta_page_post_insights`.
- **LinkedIn**: `linkedin_page_posts`. The first line before "see more" is the hook.
- **YouTube**: `youtube_channel_analytics` dimensions `["video"]`, metrics `["views","averageViewPercentage","shares"]`; the title is the hook (titles from `youtube_top_videos` or `youtube_list_recent_videos`).

Keep posts at least 3 days old. `ok: false` on a platform: say so and mine the rest.

## 2. Extract the hook

- Caption hook = the caption up to the first line break, or the first sentence if there is no break. Strip hashtags, emojis at the start, and series labels ("ep 12").
- Spoken hook = the first line the person gives you. Where both exist, keep both and note which one the viewer meets first (on-screen text and voice beat caption on reels).
- Drop posts whose hook is empty or only hashtags.

## 3. Rank (against your own medians, per platform)

Score each hook on the signals the hook actually controls:

| Signal | Why | Better is |
|---|---|---|
| Reel skip rate | did the opening stop the swipe | lower |
| Average watch seconds / watch % | did the promise hold | higher |
| Shares per 1k reach | was it worth sending | higher |
| YouTube average view % | did the title match the video | higher |

A post with reach under half the platform median can't be **proven**, whatever its ratios (one share on 200 reach is noise). If a median is 0 (common for shares on small accounts), drop that signal and score on the rest.

Hook score = number of these signals where the post beats the platform median (0-3 for reels, 0-2 elsewhere). Rank by score, then by shares per 1k. Top quartile = **proven**, bottom quartile = **failed**. Fewer than 12 posts on a platform: say the ranking is a hint only.

## 4. Bucket by pattern

Sort every hook into one pattern. Use these, add your own if a cluster clearly doesn't fit:

`number-result` (a specific outcome with a number) · `deadline` (time-bound) · `against-the-grain` (says the common advice is wrong) · `hidden-reason` (opens a gap: "why X happens") · `list` · `how-to` · `mistake-warning` · `news-or-moment` · `this-vs-that` · `direct-question` · `confession-story` (first person, something went wrong) · `call-out` (names who it's for: "for anyone who…") · `pov-scenario` ("POV: …", drops the viewer into a moment) · `explain-a-term` (defines a word the audience hears but doesn't get) · `plain-statement`.

Per pattern: n, median score, share of proven vs failed hooks. **Weight by performance, not count**: a pattern with 3 hooks all proven is worth more than one with 20 middling ones, but under 5 it is still labelled "too few to tell".

If a hooks CSV was supplied, bucket it the same way and list which patterns appear there that you've never tried. Those go to `hook-test`, not straight to production.

## 5. Remix the proven hooks

For each of the top 5 proven hooks write 3 new versions. Rule: **keep the skeleton, change the words.**

Keep from the original: its pattern, the order its clauses come in, any number (swapped only for another number that's true for this business, from `brand/facts.md` or the owner), roughly the same length and rhythm, the open question stays open (the payoff comes after the hook), the point of view.

Change: the topic noun, the verb, the emotional word, the specific detail.

Example (invented, a dog groomer):
```
proven:  "my client's poodle hadn't been brushed in 6 months. here's what we found."  [confession-story · number]
 good:   "this doodle skipped 4 grooms in a row. the undercoat told the story."
 good:   "a husky came in after 8 months without a bath. we needed two hours."
 bad:    "regular grooming is important for your dog's health."   (gap closed, number gone)
 bad:    the original line again   (a repeat, not a remix)
```

Check each remix against `brand/voice.md`. Flag any claim that needs a fact the person must confirm.

## 6. Output

**Visual (default):** fill `dashboard.html` in this folder (format in `dashboard-data.md`). `kpis`: hooks analysed, median skip rate, how many are proven. `blocks`: `bars` of patterns by median reach (top, `dim: true` for patterns with fewer than 5 hooks), a `table` of proven hooks and one of failed hooks (hook, pattern, reach, skip with `fmt: pct`), and `cards` for the remixes (tag Proven or Test, meta = the hook it came from, body = what the skeleton keeps). Show it as an artifact (claude.ai / Claude desktop), save and open it as `social-data/reports/hook-patterns-<YYYY-MM-DD>.html` (Claude Code / Cowork), or a canvas (ChatGPT). Write the verdict last, from the numbers on the page. **Chat** (settings `output: chat`, or the user asks): use the format below instead.


```
## Hook mining: <business>, <n> posts, <date range>
Ranked on: <signals used>   Spoken hooks: <yes / caption only>

### Your proven hooks (top quartile)
| Hook | Platform | Pattern | Skip % | Watch % | Shares/1k | Score |
### Your failed hooks (bottom quartile)
| Hook | Platform | Pattern | Skip % | Watch % | Shares/1k | Score |
### Patterns
| Pattern | n | Proven | Failed | Median score | Read |
### Remixes
**From:** "<proven hook>" (<pattern>, <key number>)
1. ...
2. ...
3. ...
### Patterns to test (from the CSV or untried)
- <pattern>: hand to hook-test
```

Then: which remix to use first, and which pattern to stop using. Hand remixes to `reel-script` or `caption-writer`; hand head-to-head questions to `hook-test`.

## Never

- Never ship someone else's hook verbatim, and never present the CSV's numbers as yours.
- Never put a number in a remix that the business can't back up.
- Never remix a hook that didn't perform; rank first.
- Read-only: never publish, edit or schedule from this skill.
