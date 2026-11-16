---
name: hook-test
description: Design a one-variable hook test (two openings, everything else held), declare the deciding metric and minimum sample before posting, then score it later from live Instagram or YouTube numbers pulled through Otto. Use when asked to "A/B test this hook", "which of these two openings wins", "which opening should I use", "test this hook", or "score my hook test".
license: MIT
---

# Hook test

Two modes. **Design** writes the test before anything is posted: two hooks that pull different levers, what stays fixed, which number decides, and how much data is needed. **Score** comes back later, pulls the live numbers, and calls it: A wins, B wins, or no difference. The rules are written down first so the result can't be argued into a story afterwards. Read-only; it never posts.

Tests are saved in `social-data/tests/<test-id>.md` so the score step reads exactly what was declared. No folder (claude.ai, ChatGPT): give the declaration as a block to keep in memory or a Claude Project, and ask for it back when scoring.

## Mode 1: Design

### Setup
Follow the settings and capability rules ("How every skill talks to the user" in this folder's `otto-rules.md`). In short: read `brand/settings.md` (or your memory of the user's Otto settings) first for workspace, accounts and output mode; ask only what's missing, as one multiple-choice question, and save the answers.

Then:
- Read `brand/voice.md` and `brand/winners.md` if present.
- Ask: the reel or post idea (or script), the platform, and what this post is for (stop the scroll, get shared, get saved, get comments).

### Baseline pull
To size the test, pull the account's own numbers: `meta_ig_list_media` (rowLimit about 1.2 x posts per day x 31; 40 covers one post a day) + `meta_ig_media_insights` (`views, reach, shares, saved, comments, reels_skip_rate, ig_reels_avg_watch_time`) for the last 4 weeks of reels at least 3 days old. For YouTube, `youtube_channel_analytics` dimensions `["video"]`, metrics `["views","averageViewPercentage"]`, sort `-views`. Record the median and the spread (25th to 75th percentile) of the deciding metric. Request `ig_reels_avg_watch_time` and `reels_skip_rate` only for `mediaType: VIDEO` ids (one image in the batch fails the whole call).

### Choose the design

| Option | How | Use when |
|---|---|---|
| **Paired posts** | Same video, two different hooks (on-screen text + first line), posted as two reels on matched days/times 2-7 days apart | default on Instagram |
| **Series pairs** | Run the pattern across 3+ pairs of different reels (A hook style vs B hook style) | you want a rule, not one answer |
| **Trial reels** | If the person has Instagram's trial reels, post B as a trial to non-followers | they have the feature; note that trial audiences differ |
| **YouTube title swap** | Same video, change the title after 7 days | YouTube; compare average view % for the 7 days before vs after (views fall as a video ages, so don't compare views). Where YouTube Studio offers Test & Compare for titles, use that instead |

Posting the identical video twice can be treated as a repost by the platform. Prefer changing only the first 2-3 seconds of on-screen text and voice.

### Write the two hooks
They must use **different mechanisms** (patterns from `hook-patterns`, e.g. `number-result` vs `mistake-warning`). If both pull the same lever, replace one. For each: on-screen text (≤ 8 words), first spoken line, first frame.

### Declare (write all of this before posting)

| Field | Rule |
|---|---|
| Deciding metric | One number. Stop the scroll → skip rate. Hold attention → avg watch %. Shared → shares per 1k reach. Saved → saves per 1k reach. YouTube title → average view % (not views, which fall as a video ages). |
| Minimum sample | Each version needs 1,000+ reach (skip rate, watch %) or 3,000+ reach (shares, saves per 1k, since they're rarer). Below that the score is "inconclusive". If the baseline median reach is under the minimum, say up front that one pair can't be decided and use the series design. |
| Read at | 72 hours after each post (same age for both) |
| Win threshold | A beats B by more than the account's normal spread: at least 5 points on skip rate, 15% relative on the others, AND the winner's value falls outside the 25th-75th percentile band of the baseline |
| Held constant | length, cover, caption (apart from the first line if the hook lives there), audio, hashtags, CTA, day type, time slot ±1h, no boosting |
| What we learn | If A wins: … If B wins: … If no difference: … |

Save it as `social-data/tests/<yyyy-mm-dd>-<short-name>.md` with status `designed`. Hand the hooks to `reel-script` or `caption-writer` to produce.

## Mode 2: Score

1. Read the test file. If the deciding metric or thresholds aren't written there, stop: the test wasn't declared, so it can only be reported as a comparison, not a result.
2. Ask for the permalinks (or find them by caption with `meta_ig_list_media`).
3. Pull the declared metric with `meta_ig_media_insights` for both posts (or `youtube_channel_analytics` filtered by `video==<id>` for the two date ranges). `reels_skip_rate` is already a percent; watch time is ms. Request `ig_reels_avg_watch_time` and `reels_skip_rate` only for `mediaType: VIDEO` ids (one image in the batch fails the whole call).
4. Check the posts are at the declared age (72h ± 12h). If one is far older, say so; reach keeps growing.
5. Check what wasn't held constant (different audio, a boost, a holiday). List each breach.
6. Call it:

| Result | When |
|---|---|
| **A wins / B wins** | both reached minimum sample, gap clears the threshold, no serious breach |
| **No difference** | both reached minimum sample, gap under threshold |
| **Inconclusive** | either below minimum sample, or a breach that could explain the gap |

One pair is one data point. A win becomes a rule only after the same direction shows in 3 pairs (series design).

## Output (score)

**Visual (default):** fill `dashboard.html` in this folder (format in `dashboard-data.md`). `kpis`: the deciding metric for A and for B, the minimum sample, and days since posting. `posts`: the two reels. `blocks`: a `table` comparing both arms on every metric, and `cards` with the result (tag Winner, Inconclusive or No difference) and what to do next. Show it as an artifact (claude.ai / Claude desktop), save and open it as `social-data/reports/hook-test-<YYYY-MM-DD>.html` (Claude Code / Cowork), or a canvas (ChatGPT). Write the verdict last, from the numbers on the page. **Chat** (settings `output: chat`, or the user asks): use the format below instead.


```
## Hook test: <name>   Status: <A wins / B wins / no difference / inconclusive>
Declared: <metric>, min <n> reach, read at 72h, threshold <x>
| Version | Hook | Reach | <deciding metric> | Age at read |
| A | ... |
| B | ... |
Breaches: <none / list>
What we learned: <one line, as declared>
Next: <run another pair / adopt for 3 more posts / retire pattern>
```

Update the test file to status `scored` and, if a pattern won 3 pairs, suggest a line for `brand/winners.md` and add it once the owner says yes.

## Never

- Never change the deciding metric or threshold after seeing the numbers.
- Never call a winner below the minimum sample.
- Never publish, schedule or boost the test posts from this skill.
