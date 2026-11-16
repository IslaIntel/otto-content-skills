---
name: campaign-brief
description: Write a one-page, decision-ready campaign brief (goal, audience, offer, message, channels, organic plan, paid plan, measurement) with targets set from your own numbers pulled through the Otto MCP: organic medians on Instagram, Facebook and LinkedIn, GA4 conversions, and Meta ads history (CPM, CTR, CPC, cost per result) if connected. Always produces the plan; builds paused Meta campaigns in Otto only if your connection has ads write tools and you approve, otherwise gives step-by-step Ads Manager instructions. Use when asked to "brief this launch", "plan a campaign", "make a social brief", "paid social brief", "what should this promotion say", or "how much should we spend on this".
---

# Campaign brief

A campaign is one outcome, one promise, one action, run across channels for a fixed time. This skill writes the brief everyone works from, with targets taken from what your accounts actually do, so nobody argues about made-up benchmarks later.

The brief is always produced and is read-only work. Building ads is a separate, optional step (step 4): only if this Otto connection has Meta ads write tools, only paused, and only after an explicit yes. Otherwise the paid plan comes with step-by-step instructions for Meta Ads Manager.

## 0. Setup

Follow the settings, scope and capability rules in `otto-rules.md` (in this skill's folder) ("How every skill talks to the user"). In short:
- Read `brand/settings.md` (or the assistant's memory) for workspace, accounts, default platforms and output mode. Ask only what's missing, in one bundled multiple-choice question, and save the answers.
- Plan only the channels the user named, else the defaults. `otto_list_connections` shows which of `meta_ig`, `meta_pages`, `linkedin_pages`, `ga4`, `meta` (ads; lists `selectedAdAccountIds`) are connected.
- **Capability check** (for step 4 only): does this session have Meta ads write tools (`meta_create_campaign`, `meta_create_adset`, `meta_create_ad`, ...)?
- Output is visual by default (artifact / HTML file / canvas) unless settings or the user say chat.

Also read `brand/offer.md`, `brand/audience.md`, `brand/facts.md`, `brand/voice.md`; if missing, ask and suggest `brand-brain`.

Skill questions (only what data can't tell you): **what must change, by when** (e.g. 40 consultation bookings by 15 Dec), the offer and its deadline, the landing page, budget range for ads (or "none"), and anything legal or brand-sensitive.

## 1. Pull baselines (last 90 days unless told otherwise)

**Organic**
- Instagram: `meta_ig_list_media` (rowLimit 60) + `meta_ig_media_insights` (batches of 25: `reach, views, shares, saved, comments, total_interactions`). Median reach per format (reel, carousel, image), median shares and saves per 1,000 reach, posts per week.
- Facebook: `meta_page_posts` + `meta_page_post_insights`; `meta_page_insights` for weekly `kpis`.
- LinkedIn: `linkedin_page_posts` + `linkedin_page_insights` (`kpis` and daily impressions; posts carry no per-post numbers).
- `social-data/posts.csv` if it exists saves most of these calls.

**Website**: `ga4_list_key_events` (what counts as a conversion), then `ga4_traffic_sources` for sessions and key events by channel; `ga4_landing_pages` for the campaign page's conversion rate.

**Meta ads (only if `meta` is connected)**: for each id in `selectedAdAccountIds`:
- `meta_list_campaigns(adAccountId)`: names, objective, status.
- `meta_ad_account_insights(adAccountId, startDate, endDate, fields: ["spend","impressions","reach","clicks","ctr","cpc","cpm","frequency","actions","cost_per_action_type"])`.
- `meta_campaign_insights(campaignId, ...)` with the same fields for the 2-3 past campaigns whose objective matches this one. Account-wide averages mix objectives; a campaign of the same type is the better baseline (CPM can differ several-fold between them).
- `actions` and `cost_per_action_type` list many overlapping types (`lead`, `offsite_conversion.fb_pixel_lead`, `onsite_web_lead`, `complete_registration`, `purchase`...). Pick the **one** that matches this campaign's goal and the GA4 key event; never add overlapping types together. Ask the user if unsure which one they count.
- An account that returns 0 rows has no history: say "no paid baseline" and plan a small learning budget instead of a forecast.

Fallback: any `ok: false` is named in the brief under "Missing data" and the brief continues. Never fill a gap with an industry benchmark.

## 2. Decide

1. **One outcome, one number, one source.** "Bookings counted as GA4 key event X." If it can't be measured, change the goal or set up tracking first (`utm-builder`).
2. **Work back from the target.** Using the baselines: conversions needed ÷ landing page conversion rate = sessions needed. Split sessions between organic (what your channels usually send per week × campaign weeks) and paid (the rest). Paid sessions × your cost per landing page view or CPC = paid budget implied. If the implied budget is above the user's range, say so plainly and offer a smaller target or a longer window.
3. **Message.** Audience situation (in their words, from `brand/audience.md` or `comment-mining`) → the promise → the proof you're allowed to use (`brand/facts.md`, `social-proof-finder`) → the one action. Write 3 message angles; each becomes a creative test.
4. **Channel roles.** Give each connected channel a job, not a copy of the same post:

| Channel | Job in this campaign | Format that works for you (from data) | Posts |
|---|---|---|---|

5. **Organic plan.** Weeks before / during / last call. Use your best format per the medians. Hand the posts to `content-calendar`; reels to `viral-reel-planner`; captions to `caption-writer`; keyword comments to `comment-to-lead`.
6. **Paid plan.** Objective, audience hypothesis (who, not targeting settings), creatives (best organic posts by shares/saves per 1,000 reach are first candidates), budget and dates if the user gave them, test design (one variable), and stop rules: e.g. "pause an ad after spend = 2x your target cost per result with zero results". Mark budget "open" if the user didn't give it.

## 3. Output: the brief

Default is visual (artifact / HTML file / canvas) unless settings or the user say chat. Content:

```
CAMPAIGN: <name>   Dates: <start-end>   Owner: <name>
GOAL: <number> <event> by <date>, counted in <source>
WHY NOW: <one line>
AUDIENCE: <situation + their words>
OFFER: <what, price if public, deadline>    LANDING PAGE: <url>
PROMISE: <one sentence>   PROOF ALLOWED: <list>   CAN'T SAY: <list>
ACTION: <the one thing we ask>
ANGLES TO TEST: 1. ... 2. ... 3. ...

YOUR BASELINES (last 90 days)
| Channel | Metric | Your median | Source |
| Meta ads (similar campaigns) | CPM / CTR / CPC / cost per <event> | ... | meta_campaign_insights |

THE MATH: target ÷ landing CVR <x%> = <n> sessions → organic ~<n> + paid ~<n> → budget implied ~<amount>
CHANNEL ROLES: <table>
ORGANIC PLAN: <week-by-week table>
PAID PLAN: objective / audience hypothesis / creatives / budget / test / stop rules
TRACKING: UTM pattern, GA4 key event, Meta result type
REVIEW DATES: day 3 (delivery), day 7 (first read), end (campaign-retro)
MISSING DATA / OPEN QUESTIONS: <owner for each>
```

Save it as `campaigns/<yyyy-mm>-<name>.md`. After the campaign, run `campaign-retro` against this file.

## 4. Optional: set up the paid plan

- **Ads write tools available**: offer to build it in Otto. Show every object first (campaign objective and name, ad set budget, dates, audience, placements; each ad's creative, text, link with UTM). On a yes: `meta_create_campaign`, `meta_create_adset`, `meta_create_creative` / `meta_create_video_creative`, `meta_create_ad`, each with `params.status: "PAUSED"` (Marketing API params). The user turns them on in Ads Manager after checking. Report the ids created; if a call fails, stop and report, don't retry in a loop.
- **No ads write tools**: give numbered steps for Meta Ads Manager: create campaign (objective), ad set (budget, schedule, audience hypothesis as settings, placements), ads (which creative, primary text, headline, link with UTM), stop rules as rule reminders. Leave it paused until reviewed.

## Never

- Create anything in an ad account without an explicit yes on the exact objects, or create it anywhere but paused.
- Edit, launch or turn on existing campaigns, ad sets or ads.
- Promise a result: targets are estimates from past numbers and are labelled that way.
- Add overlapping Meta action types or mix organic and paid numbers in one figure.
- Use an industry benchmark where the user's own number exists, or invent one where it doesn't.
