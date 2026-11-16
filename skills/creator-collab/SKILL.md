---
name: creator-collab
description: Plan a creator, influencer or UGC collaboration end to end, as drafts only (you send every message yourself): decide if a creator fits using evidence from what they post, write the first message, write the brief they film from, cover usage rights and disclosure, and measure the result with your own Otto data (UTM links, GA4, Instagram insights on the collab post). Use when asked "is this creator a good fit for us", "draft my first message to a creator", "pitch a collab", "UGC brief", "brief my videographer", or "did the collab work".
license: MIT
---

# Creator collab

One skill, five modes. Run the one the user needs, or all five in order for a new partnership. A creator is a test with a cost, so every collab gets a measurable goal before anyone is contacted.

Otto can't read another account's numbers. Evidence about the creator comes from the user (links, screenshots of their insights, a media kit). **This skill only drafts.** It never contacts a creator, sends a message, DM or email, or follows up. You send every message yourself, from your own account or inbox.

## 0. Setup

Follow the settings, scope and capability rules ("How every skill talks to the user" in this folder's `otto-rules.md`). In short:
- Read `brand/settings.md` (or the assistant's memory) for workspace, accounts and output mode. Ask only what's missing, in one bundled multiple-choice question, and save the answers.
- Measure only the platforms the collab runs on.
- Output is visual by default (artifact / HTML file / canvas) unless settings or the user say chat. Message drafts are also given as plain text to copy.

Also read `brand/offer.md`, `brand/audience.md`, `brand/voice.md`, `brand/facts.md`; if missing, ask what you sell, who buys, and what you can and can't claim, and suggest `brand-brain`.

Skill questions: the goal (sales, leads, followers, content to reuse in ads), budget or what you can offer (fee, product, commission), and the creator's handle or links.

**Your baseline** (so you know what "good" means): `meta_ig_list_media` + `meta_ig_media_insights` (`reach, views, shares, saved, comments`) for posts at least 3 days old from the previous 28 days → median reach (your usual) and shares per 1,000 reach. If GA4 is connected, `ga4_traffic_sources` for last 28 days: sessions and key events from Organic Social.

## Mode 1: Fit check

Ask the user for the creator's last 10-12 posts (links or screenshots) and, if offered, their insights screenshot (reach, audience country, age).

| Check | Pass | Red flag |
|---|---|---|
| Audience | Comments come from people like your buyers (location, job, problem) | Comments are emoji, other creators, giveaways |
| Topic | They already talk about your problem or a neighbour of it | You'd be the odd post out |
| Format | They make the format you need (talking head, demo, tutorial) | Only aesthetic shots when you need a demo |
| Consistency | Views per post hold within a range | One viral post, the rest a tenth of it |
| Trust | They disclose paid posts; past sponsors fit their niche | Five unrelated sponsors this month |
| Conflict | No direct competitor in the last 90 days | Promoted a competitor recently |

Score each Pass / Unclear / Fail. Any Fail on Audience or Conflict = don't approach. Label every point "seen in their posts" or "assumed". Follower count is not a criterion. Cost check: fee ÷ (their typical views / 1,000) gives their cost per 1,000 views; compare it with your ads CPM (cost per 1,000 impressions, from `campaign-plan` if Meta ads are connected). Impressions and views aren't the same, so treat it as a rough check.

## Mode 2: First message

Inputs: one specific post of theirs the user has actually watched. If none, stop: "Watch two of their recent posts first and tell me one thing you noticed."
1. Line one: that specific thing, in a sentence only someone who watched could write.
2. Why their audience would care about your offer (not why you want them).
3. The idea, concrete enough to picture: what they'd film, roughly how long.
4. What's on offer: fee, product, commission, or "budget to be agreed". Never hide that it's paid.
5. One easy yes/no question. Easy to decline.
A draft for you to send. Under 120 words. One follow-up draft for 7 days later that adds something new (a detail, a sample); no third message. Send through the contact route they list for business (email in bio, management); DM only if they invite it.

## Mode 3: The brief

```
COLLAB BRIEF: <business> x <creator>    Deadline: <date>
GOAL: <the one number this is judged on>
WHO WATCHES: <their audience, in a sentence>
THE IDEA: <2 lines>
HOOK (written out, first 2 seconds): say "<words>" / show "<shot>"
BEATS: 1. <beat>, point: <why it's there> ... (let them say it their way)
MUST INCLUDE: <product moment, offer, keyword or link>
MUST NOT: <claims you can't make, words you never use, competitors>
DISCLOSURE: paid partnership label on / #ad in first line of caption
DELIVERABLES: length, 9:16, raw + edited, captions burned in or not, file format, where to send
POSTING: date, collab post (both accounts) yes/no, link: <UTM link from step below>
REVIEW: one round of changes for factual errors, within <48h>
```
Use `hook-writer`, `reel-script` and `shot-list` for the hook and beats if the user wants them written out. For UGC (filmed for you, posted by you), drop POSTING and add "3 hook variations, same body" so you can test them.

## Mode 4: Rights and disclosure checklist

Agree in writing before filming:
- [ ] Fee, product, commission and when it's paid
- [ ] Where you may reuse it (your organic, your ads, website, email) and for how long
- [ ] Whether you can run it as a partnership ad from their handle, and for how long
- [ ] Edits you may make (cut, subtitle, crop) and what needs their OK
- [ ] Exclusivity: competitors they won't promote, for how long (paid separately if long)
- [ ] Disclosure: platform's paid partnership label plus a clear word in the caption
- [ ] Raw files delivered, and who owns them
- [ ] Music: licensed for commercial use, or added by you later
This is a checklist, not legal advice; for big deals, a lawyer reads the contract.

## Mode 5: Measure it

Before posting, set up: a link from `utm-builder` (`utm_source=instagram&utm_medium=creator&utm_campaign=<creator>-<yyyymm>`) and, if useful, a code unique to them.

7 and 28 days after posting:
- **Collab post on your account** (Instagram collab or a reel you posted): find it with `meta_ig_list_media`, then `meta_ig_media_insights` (`views, reach, shares, saved, comments, ig_reels_avg_watch_time, reels_skip_rate`). Compare with your median. Request `ig_reels_avg_watch_time` and `reels_skip_rate` only for `mediaType: VIDEO` ids (one image in the batch fails the whole call). If the post isn't in your media list, it's the creator's post: only they see its insights, so ask them for a screenshot.
- **Your account**: `meta_ig_account_insights` (`metricType: time_series`, `reach`, `follower_count`) for 7 days before vs 7 days after (`endDate` = last day + 1; end dates are exclusive). `follower_count` is daily new follows and only exists at 100+ followers.
- **Website**: `ga4_run_report` with dimension `sessionCampaignName` (or `sessionSource`) filtered to the campaign, metrics sessions and key events.
- **Their side**: ask the creator for a screenshot of their post insights (reach, link clicks, story taps).
- Codes and sales: from the user's store.

| Metric | Result | Your baseline | Verdict |
|---|---|---|---|

Cost per result = fee ÷ key events (or ÷ sales). Verdict: repeat, change one thing, or stop. If ads are planned with the content, hand off to `campaign-plan`. Fallback: tools returning `ok: false` are named and skipped; never estimate a number you didn't get.

## Never

- Contact a creator, or send any message or follow-up, on the user's behalf. Drafts only.
- Claim audience data, reach or sales the user didn't supply.
- Write a brief that asks a creator to make claims you can't support, or to hide that it's paid.
- Reuse their content beyond what was agreed.
