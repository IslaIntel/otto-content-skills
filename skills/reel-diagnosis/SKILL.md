---
name: reel-diagnosis
description: Diagnose why an Instagram Reel over- or under-performed, using your own account's numbers pulled through the Otto MCP. Use when someone asks "why did this reel flop", "why did this one work", "what went wrong with my last video", or wants to compare two reels.
license: MIT
---

# Reel diagnosis

Judge every reel against **your own baseline**, never against industry benchmarks or someone else's screenshot. A reel is good or bad compared with what your account usually does.

This is the per-reel detail view: `weekly-social-review` and `daily-pulse` embed its result for each reel they flag inside their own dashboards. Run on its own, it produces one reel card.

Read-only. This skill never posts, deletes, replies or hides anything.

## 0. Setup

Follow the settings and scope rules in `otto-rules.md` (in this skill's folder) ("How every skill talks to the user"). In short: read `brand/settings.md` (or your memory of the user's Otto settings) first for workspace, Instagram account and output mode; ask only what's missing, as a multiple-choice question, and save the answer. If the workspace has more than one Instagram account (`meta_page_list`), ask which one.

## 1. Get the numbers (Otto MCP)

1. Find the Instagram account from settings (or `otto_list_connections`).
2. `meta_ig_list_media` (rowLimit 60) to find the reel(s) by caption, link or date, plus every reel from the last 4 weeks for the baseline.
3. `meta_ig_media_insights` in batches of up to 25 ids, metrics:
   `views, reach, likes, comments, shares, saved, total_interactions, ig_reels_avg_watch_time, reels_skip_rate`.
4. Ask for the reel's length in seconds if you can't see it, and what's on screen in the first second and the first spoken line. If the person can share the video or a screenshot of Instagram's retention graph, use it.

Data you must convert correctly:

- `ig_reels_avg_watch_time` is in **milliseconds**. Divide by 1,000 for seconds, then by the reel length for watch %.
- `reels_skip_rate` is already a percent (29 means 29%).
- Per-reel follows and profile visits are **not** available from the API for reels. Don't invent them; ask for an in-app screenshot if they matter.

## 2. Build the baseline

Baseline = the **median** of reels from the previous 4 weeks that are at least 3 days old (reach mostly settles by then). Leave out image posts and anything the person says was a one-off (a test, a meme, a paid boost). Compute for each reel:

- skip rate, watch %, average watch seconds
- shares per 1,000 reach, saves per 1,000 reach, comments per 1,000 reach

With fewer than 5 baseline reels, say the baseline is thin and treat every conclusion as a hint. If posting cadence or format changed inside the 4 weeks, also show the median of reels from the same stretch as this reel, and judge against that one.

A reel under 3 days old gets an "early read" only.

## 3. Walk the tree, stop at the first failing step

In the dashboard's `steps`, everything after the first `fail` is `skip` ("not judged"): once a step explains the flop, later steps aren't evaluated. For an over-performer, mark each step `pass` where it beat the baseline.

1. **Skip rate worse than baseline** → the first frame or the first line failed. Quote the first line, describe the first frame, and propose one new hook.
2. **Skip fine, watch % worse than baseline** → pacing or length. Without the reel's length, don't judge this step from average watch seconds alone (a shorter reel always has fewer); compare only with reels of similar length or ask for the length. If there's a retention graph, name the second people leave and what was on screen then.
3. **Watch % fine, shares per 1,000 reach low** → nothing worth sending to a friend. Name who this reel would be sent to; if nobody, say so. **If your usual shares per 1,000 reach is 0** (common on small accounts), this step can't tell reels apart: mark it `skip` ("not judged"), never `fail`, say why in the evidence, and go on to step 4.
4. **Reach good, follows low** → no reason to follow. Does the reel promise more (a series, a part 2)? Does the profile match what the reel showed? (Use `profile-check`.)
5. **Reach tiny on everything that week** → distribution, not content. Check muted or licensed audio, a missing video, a restriction, reposted material, or a posting gap.

If the reel **over**-performed, run the same tree in reverse: which step did it beat the baseline on? That's the thing to repeat.

## 4. Output

**Run alone (default): a single-reel visual card.** Fill `dashboard.html` in this folder (see `dashboard-data.md`) with this reel as the only item in `posts` (its `diagnosis` filled in), 3 KPIs (reach, skip rate, watch vs the baseline) and `meta.focusPost` set to the reel's id so the diagnosis opens on load. Show it as an artifact (claude.ai / Claude desktop), an HTML file opened in the browser (Claude Code / Cowork), or a canvas (ChatGPT). The card shows: reel link and date, verdict, the five tree steps with the failing (or winning) one highlighted, each metric next to its baseline median (skip rate, watch % or watch seconds, shares/saves/comments per 1k reach), the evidence line, and one change to try next. Two reels: two cards side by side.

**Chat mode** (settings `output: chat`, or the user asks): the same content as a table:

| Reel (link) | Verdict | Failing (or winning) step | Evidence vs baseline | One change to try next |

**Embedded** (called from `weekly-social-review` or `daily-pulse`): return just that row's content; the calling skill places it in its own dashboard.

Then one line: what you'd test on the next reel, changing only one thing.

Rules:
- One reel never proves a cause. Say "this suggests", not "this proves".
- Keep what was measured apart from what you think caused it.
- "Not enough data to tell" is a valid answer.
