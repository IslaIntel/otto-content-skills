---
name: content-engine
description: One command that runs the whole content pipeline in order, from your real Otto data to a planned and approved reel that gets posted (through Otto scheduling, a posting queue or by hand, depending on your connection), with a comment-to-lead loop and a measurement date, by calling the other skills in this pack. Stops for your approval at each decision. Use when asked to "run the content engine", "do the whole thing", "make me a reel from start to finish", "set up my content system", or "plan and make this week's reel".
license: MIT
---

# Content engine

Every other skill in the pack handles a single step. This is the conductor: it calls them in order, hands each result to the next step, and pauses wherever you need to decide. It needs nothing beyond Claude and the Otto MCP. If you automate DMs, it hands you the DM flow to load into a DM tool yourself; it never sets one up. Filming and editing are done by you (or your editor); everything around them is prepared here.

Every write (publishing, scheduling, replying) happens only after an explicit yes on the exact content, in this conversation, and only through tools this connection actually has.

## 0. Setup (first run only)

Follow the settings, scope and capability rules ("How every skill talks to the user" in this folder's `otto-rules.md`). In short:
- Read `brand/settings.md` (or the assistant's memory) for workspace, accounts, default platforms, timezone and output mode. Ask only what's missing, in one bundled multiple-choice question, and save the answers.
- Scope = the platforms the user named, else the defaults; ask once if there are none ("All connected" as an option). Instagram (`meta_ig`) is the core. A platform in scope that isn't connected is mentioned every run, with `otto_connect_link` (LinkedIn: connect it in Otto's settings).
- **Capability check**: look at which Otto tools this session has (or `otto_list_connections`) once, and note it: scheduling (`channel_submit_plan`), publish (`meta_ig_publish_reel`, ...), comment replies (`meta_ig_reply_comment`, ...). Each step below uses that note; don't promise a write the connection can't do.
- Output is visual by default (artifact / HTML file / canvas) unless settings or the user say chat.

Skill questions: how many pieces this run (default 1 reel), the comment keyword if they use one, and the deadline.

## The pipeline

| # | Step | Skill | What it hands on | Stop? |
|---|---|---|---|---|
| 1 | Memory check | `brand-brain` | `brand/` files exist and are under 90 days old. If missing or stale, run it first. | Only if `brand/` is missing |
| 2 | Where we stand | `weekly-social-review` (once a week) or `daily-pulse` (other days) | Baselines, last winners, the one change to make | No |
| 3 | Ideas | `topic-finder` + `trend-radar` | 5-10 ideas tied to evidence (search queries, comments, your winners) | No |
| 4 | Pick and plan | `viral-reel-planner` | 3 reel concepts, each with why it should work for you | **STOP A**: you pick one |
| 5 | Hook | `hook-writer` | 5-10 hooks for the concept, ranked; one recommended | **STOP B**: you pick one |
| 6 | Script | `reel-script` | Beat-by-beat script, length, on-screen text | No |
| 7 | Shots | `shot-list` | What to film, in order, with framing | No |
| 8 | Caption | `caption-writer` | Caption (keyword CTA only if the CTA setting allows it), alt text | No |
| 9 | Human pass | `sound-human` | Script and caption cleaned of AI tells | No |
| 10 | Cover | `cover-designer` | Cover built in code from your frame and text | No |
| 11 | Review pack | (this skill) | Everything above on one page | **STOP C**: you approve or edit |
| (you) | *You film and edit* | | The video goes into the Otto media library | Wait for the user |
| 12 | Post | `posting-plan`, then Otto scheduling, `post-queue` or by hand | A time slot from `best-time-to-post` data, then the post going out by the path this connection allows | **STOP D**: yes to publish, schedule or queue |
| 13 | Leads | `comment-to-lead` | Comments sorted, replies drafted (sent via Otto if reply tools exist), DM flow ready for a DM tool | **STOP E**: yes to send replies |
| 14 | Measure | `daily-pulse` (day 1-2), `reel-diagnosis` (day 3+) | Verdict vs baseline, one change for next time | No |
| 15 | Remember | `brand-brain` | Winners appended to `brand/winners.md` | Only to approve the lines brand-brain proposes |

Run steps 2-11 in one go, pausing only at STOP A, B and C (and at step 1 if `brand/` is missing). Steps 12-15 happen after filming, often in a later session: say which step to resume from.

## Rules between steps

- **Pass forward, don't re-ask.** Each skill gets the previous step's output and the `brand/` files. Ask the user only for things no step can produce.
- **Evidence travels.** The reason an idea was picked (e.g. "your 3 best reels this month were how-tos under 30 s") is written into the plan, the script and the review pack, so it can be checked in step 14.
- **One change per run.** If step 2 named a change (shorter reels, new hook style), apply it here and nothing else new, so step 14 can tell if it worked.
- **Original only.** Borrow the structure of a format, never another creator's words or footage.
- **The CTA must be kept.** If the caption says "comment GUIDE", the guide exists and step 13 is planned before posting.
- If a step's data pull fails (`ok: false`), it says so and the engine continues with what it has. No invented numbers anywhere in the chain.

## STOP C: the review pack

```
REEL: <working title>          For: <audience>      Why this one: <evidence from step 2-4>
HOOK (0-2 s): say "<line>" / show "<frame>" / text "<on-screen>"
SCRIPT: <beats with timing>     LENGTH: <s>
SHOT LIST: <numbered>
COVER: <text> on <frame>
CAPTION: <full caption>         KEYWORD: <word> → delivers <thing>
POST: <platform(s)>, <day/time + zone>, reason: <best-time data>
SUCCESS = <metric> above <your median value> by day 3
```
Ask: "Approve this pack, or tell me what to change?"

## STOP D: publish, schedule or queue

Show the final caption, the media, the cover and the time. On a yes, take the first path this connection allows:
1. **Otto scheduling** (only if your Otto connection includes `channel_submit_plan`): video in the Otto library (`media_list`), then `channel_submit_plan` (provider `meta_ig`, op `ig_publish_reel`, `publishAt` with offset, `timeZone`). It returns an `approveUrl` unless the workspace auto-approves; say "scheduled" only if the result says `scheduled: true`. `otto_schedule_list` confirms.
2. **Publish tools, no scheduling**: post now with `meta_ig_publish_reel` (mediaId, caption, optional coverMediaId or thumbOffsetMs, `confirm: true`; the cover can only be set at publish) and, for Facebook, `meta_page_publish_video` (pageId, mediaId, the caption as `description`, `confirm: true`; Facebook Reels must be 3-90 s), or for a later time hand it to `post-queue`.
3. **Neither**: give the user the video, cover, caption and time, and the steps to post it in the app.

## Daily or weekly rhythm

- **Monday**: steps 1-11 for the week's pieces (`weekly-social-review` in step 2), then `posting-plan` for slots.
- **Each posting day**: steps 12-13 for that piece (or let `post-queue` publish it); `comment-to-lead` once in the morning and once late afternoon while the post is fresh.
- **Day 3 after each post**: step 14. **Friday**: step 15.
A sustainable number of posts beats an ambitious one; set the count from what the user actually filmed last month.

## Never

- Publish, schedule, queue or reply without a yes on the exact content.
- Promise scheduling or replies before the capability check shows the tools exist.
- Skip a STOP because the user said "do everything" once; each STOP is for that piece.
- Claim a reel is filmed, uploaded, published or scheduled unless a tool result shows it.
- Set up anything that replies or messages people automatically, or use browser automation.
