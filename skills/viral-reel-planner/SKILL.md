---
name: viral-reel-planner
description: Plan a short-form video (Instagram Reel, YouTube Short, TikTok) backwards from the one result you want, building the hook checklist from your own winners and losers pulled through the Otto MCP (skip rate, watch time, shares, saves). Use when someone says "help me go viral", "plan a reel", "I have an idea for a video", "how do I get more shares", "my reels get no views", or "what should my next reel be".
---

# Viral reel planner

Turns an idea into a one-page plan: the goal, the feeling that makes people take that action, the format, the hook, the payoff and the next step. Most reels fail because they try to get views, saves, follows and leads at once. This skill makes you pick one.

"Viral" here means "spreads further than your usual reel", measured against your own median, not a famous creator's numbers.

Read-only on every platform. Hands off to `hook-writer`, `reel-script`, `shot-list`, `cover-designer` and `caption-writer` for the build.

## 1. Setup
Follow the settings, scope and capability rules in `otto-rules.md` (in this skill's folder) ("How every skill talks to the user"). In short: read `brand/settings.md` (or memory) for workspace, accounts and output mode; ask only what's missing in one multiple-choice message and save it. Scope is the platforms the user names, else the defaults in settings. Output is visual by default (artifact / HTML file / canvas) unless settings say chat.

- Read `brand/` (voice, audience, offer, facts, winners). If it's missing, ask: what you sell, who it's for, the one action you want, and three words for how you sound. Suggest running `brand-brain` once.
- Ask for the idea in one sentence, if they haven't given it.

## 2. Pull your own evidence
- `meta_ig_list_media` (rowLimit 60) and `meta_ig_media_insights` in batches of 25: `views, reach, likes, comments, shares, saved, ig_reels_avg_watch_time, reels_skip_rate`. Reels at least 3 days old only. Request `ig_reels_avg_watch_time` and `reels_skip_rate` only for `mediaType: VIDEO` ids (one image in the batch fails the whole call).
- If `brand/winners.md` is under 2 weeks old, use it and only pull reels posted since.
- YouTube Shorts: `youtube_top_videos` (last 90 days) for views and averageViewDuration; `youtube_channel_analytics` with dimension `video` and metrics `views, averageViewPercentage, subscribersGained, shares` for which videos earned subscribers.
- Ask the reel length and first spoken line for the top and bottom 5 if they aren't in `brand/winners.md`. The API doesn't return length.

**Second source: other accounts' reels (comparison only).** If `meta_ig_business_discovery` is in the tool list, pull recent reels from accounts the user names (or that `trend-radar` found) with their likes and comments. Otherwise use examples the user supplies (links or files), analysed with `reel-breakdown`. Your own winners stay the primary evidence; other accounts show formats and hook shapes worth trying, never wording to copy.

Units: watch time arrives in **milliseconds**; skip rate is already a **percent**. No Instagram metric shows follows or profile visits per reel; ask for an in-app screenshot if the goal is follows.

Not connected or `ok: false`: say so, then plan from principles only and label the hook checklist "not yet checked against your data".

## 3. Pick ONE goal

| Goal | The number that proves it | The feeling that drives it | Formats that fit |
|---|---|---|---|
| Reach (strangers) | reach vs your median, skip rate | surprise, "wait, what?" | one-scene story, a reveal, a before/after |
| Shares | shares per 1,000 reach | "this is so them", being right, being early, a laugh at a shared pain | relatable skit, a hot take, "for the friend who..." |
| Saves | saves per 1,000 reach | relief at a problem solved, fear of forgetting | checklist, steps, a template, a cheat sheet |
| Follows | new follows that day (`meta_ig_account_insights` `follower_count`), YouTube `subscribersGained` | wanting the next one | a numbered series, a recurring character or format |
| Leads | comments with the keyword, DMs, bookings | wanting the specific thing you offer, now | a result shown, the method held back for the DM |

If they name two goals, ask which matters this week. A lead reel is judged on DMs and bookings, not views.

## 4. Build the hook checklist (principles + your data)

Start with these principles:
1. Something is already happening in the first frame. No logo, no fade, no "hey guys".
2. The viewer recognises their own situation within 1 second.
3. The first spoken word arrives within half a second and names the subject.
4. On-screen text says the hook on its own, for people with the sound off. Big, high contrast, inside the safe area.
5. It opens a question the reel answers by the end, and the answer is real.
6. It's about the viewer's problem, not the business.

Then add what **your** account shows. Split your reels at the median skip rate and compare the low-skip half with the high-skip half on: first-frame type (face, product, text card, screen), first line form (question, number, "for anyone who...", statement), length, and topic. Write a line only when the gap holds across at least 5 reels on each side:

`On your account, reels that open on <x> skipped <a>% vs <b>% for <y> (n = 6 vs 9).`

Fewer than 5 per side: "too few to tell yet". Keep principles and data-backed lines visibly separate.

From other accounts' examples, add at most 2 lines marked "seen elsewhere, not yet tested on your account" (for example a format or first-frame type that recurs in their top reels). They rank below your own data lines.

## 5. Plan the reel

1. **Feeling**: from the goal table, in one line, for this idea.
2. **Format**: pick from the table; prefer a format that appears in your winners.
3. **Hook**: draft 3 (or run `hook-writer` for 10). Score each against the checklist; keep the one that passes the most, with the data lines weighted above principles.
4. **Hold**: one question kept open until the payoff. If the reel is longer than your median average watch seconds, add a turn (a new fact, a twist, a number reveal) every 4 to 6 seconds.
5. **Payoff**: the thing the hook promised, delivered on screen. If you can't show it truthfully, change the hook.
6. **Next step**: one call to action that matches the goal (send it to someone / save it / follow for part 2 / comment a word for the guide). For a comment keyword, confirm what the DM delivers and hand off to `comment-to-lead`.
7. **Length target**: aim for your median average watch seconds plus 30%, unless the format needs more. Say the number.

## 6. Output

Default is visual (artifact / HTML file / canvas); chat if settings or the user say so.

```
REEL PLAN: <idea in one line>
Goal: <one>  -> judged by <metric>, your median is <x>
Feeling: <one line>
Format: <format> (your winners in this format: <n>)
Hook (chosen): spoken "<line>" | first frame: <what's moving> | text: "<on-screen text>"
  Checklist: principles 6/6 | your data: <lines it passes / fails>
Hold: <the open question> | turns at ~<s>s, ~<s>s
Payoff: <what's shown, and that it's true>
Next step: <CTA> -> delivers <thing>
Length: <s>s (your median watch <s>s)
Evidence used: <n> of your reels, <date range>; other accounts: <n examples, source>. Too few to tell on: <list>
Next: hook-writer -> reel-script -> shot-list -> cover-designer -> caption-writer
```

After it posts, run `reel-diagnosis` at 3 days and add the result to `brand/winners.md` via a `brand-brain` wrap-up.

## Never
- Promise a payoff the reel doesn't deliver, or a DM that won't arrive.
- Put a number on screen that isn't in `brand/facts.md` or the pull.
- Copy another creator's script, voice or footage. Learn the structure, write your own.
