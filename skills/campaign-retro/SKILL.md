---
name: campaign-retro
description: Look back at a finished campaign or launch using everything Otto can pull for its date window (posts and their numbers on Instagram, Facebook, LinkedIn and YouTube; GA4 sessions, landing pages and UTM campaigns; Meta ads insights when this connection can read them) and decide what to repeat, change and stop. Use when asked to "run a retro", "was the launch worth it", "postmortem this campaign", "should we do this again", or "how did the promo do".
license: MIT
---

# Campaign retro

Takes a campaign that has ended and turns it into a short list of repeat / change / stop decisions, each tied to a number. It compares the campaign window with the weeks before it, so "it did well" means "better than your normal". It records facts, then explanations, then decisions, and keeps them separate. Read-only.

## 0. Setup

Follow the settings, scope and capability rules in `otto-rules.md` (in this skill's folder) ("How every skill talks to the user"). In short:
- Read `brand/settings.md` (or your memory of the user's Otto settings) first: workspace, accounts, default platforms, output mode. Ask only what's missing and save the answers.
- Scope is the platforms the user names; otherwise the default from settings; otherwise ask once, listing connected platforms plus "All connected". A platform with nothing in the window gets one line, never an empty table.
- **Meta ads capability check**: include paid results only if this session has Meta ads read tools (`meta_list_campaigns`, `meta_campaign_insights`) and `otto_list_connections` shows `meta` connected. Otherwise run organic + GA4 only and say "Paid ads not included: this connection can't read Meta ads."

If a `campaigns/*.md` brief from `campaign-plan` exists for this campaign, read the goal, target, dates and UTM names from it and ask only what it doesn't answer.

Ask (one message, multiple choice where it fits):
- Campaign name, **start and end date**, and what it was meant to do (sales, signups, bookings, followers, awareness), with any target set beforehand.
- Which posts, ads and links belonged to it: hashtags, a caption phrase, UTM campaign name, Meta campaign name. If there's a `social-data/utm-log.csv` from `utm-builder`, read it.
- Anything else that happened in the window (a sale, a holiday, press, a site outage, a price change).

Read `brand/offer.md` for the intended action.

Windows: **campaign** = start to end + 7 days of tail. **Baseline** = the same number of days just before the start. If the tail runs past yesterday, report the days available, mark the rest "not yet available", and give the date to re-run for the full read. Only include ad campaigns that belong to this campaign (ask if unsure; never assume every active campaign is part of it).

## 1. Pull (both windows)

**Organic posts**
- Instagram `meta_ig_list_media` (rowLimit about 1.2 x posts per day x days covered by the campaign and baseline windows; read it with code if saved to a file) → `meta_ig_media_insights` (`views, reach, likes, comments, shares, saved, ig_reels_avg_watch_time, reels_skip_rate`). `meta_ig_account_insights` time_series `reach`, `follower_count` (daily new follows, 100+ followers only). Request `ig_reels_avg_watch_time` and `reels_skip_rate` only for `mediaType: VIDEO` ids (one image in the batch fails the whole call).
- Facebook `meta_page_posts` → `meta_page_post_insights`; `meta_page_insights` for weekly kpis.
- LinkedIn `linkedin_page_posts`, `linkedin_page_insights`.
- YouTube `youtube_top_videos`; `youtube_channel_analytics` dimensions `["day"]`, metrics `["views","subscribersGained"]`.

**Website (GA4)**
- `ga4_run_report` dimensions `["sessionSource","sessionMedium","sessionCampaignName"]`, metrics `["sessions","engagedSessions","keyEvents"]`. This is where UTM-tagged links show up; filter on the campaign name if known.
- `ga4_run_report` dimensions `["landingPage"]`, same metrics, filtered to the campaign or to the campaign's landing pages.
- `ga4_traffic_sources` for channel totals in both windows.

**Paid (only if the capability check passed)**
- `meta_list_campaigns` to find the campaign by name; `meta_campaign_insights` with fields `["spend","impressions","reach","clicks","ctr","cpc","actions"]`. `actions` is a list of `{action_type, value}`: pull out `landing_page_view`, `link_click`, and the conversion type the campaign optimised for (e.g. `complete_registration`, `purchase`, `lead`).

**Sales / signups** live outside Otto unless Shopify is connected (then `shopify_list_orders`, if it's in the tool list). Ask for the count if needed. If a call returns `ok: false`, list it under "missing" and go on.

## 2. Reconstruct

A dated timeline: every post, ad start/stop, email, price change and outside event, next to daily site sessions and key events. A spike that starts before the post that "caused" it was caused by something else.

## 3. Read the evidence

Per channel: campaign window vs baseline, and against the target if there was one.

| Question | Evidence |
|---|---|
| Did people see it? | reach / views vs baseline median per post |
| Did it hold them? | skip rate, watch %, shares per 1k |
| Did they come to the site? | sessions by source/campaign, landing page sessions |
| Did they act? | key events, signups/sales, Meta conversion actions, cost per result |
| Did it last? | baseline vs the 7-day tail: did sessions and follows return to normal or stay higher |

Check the tracking itself: UTM-tagged sessions vs untagged social sessions (`facebook.com`, `m.facebook.com`, `l.facebook.com`, `lm.facebook.com`, `meta`, `ig`, `instagram.com`, `l.instagram.com` referrals). Campaign names that appear in mixed case or with typos are split rows in GA4: add them up and flag it for `utm-builder`.

## 4. Facts, explanations, decisions

1. **Facts**: only numbers and events.
2. **Explanations**: each one a hypothesis with a confidence (low / medium / high) and the evidence that would confirm it next time.
3. **Decisions**: at most 3 each of repeat / change / stop. Each cites a fact. Add one **test** for the biggest open question, designed with `hook-test` or the next `campaign-plan`.

Include what flopped and what couldn't be measured.

## 5. Output

**Visual (default):** fill `dashboard.html` in this folder (format in `dashboard-data.md`). `kpis`: the campaign window vs the same-length baseline (reach, site visits, follows, key events; spend and cost per result only if ads data was included). `daily`: sessions or reach per day across both windows. `posts`: the campaign's posts with their status. `blocks`: a `table` of traffic by source / UTM campaign (sessions, engaged sessions, key events), and a `list` of tracking fixes. `plan`: keep (repeat), change, stop. Show it as an artifact (claude.ai / Claude desktop), save and open it as `social-data/reports/campaign-retro-<YYYY-MM-DD>.html` (Claude Code / Cowork), or a canvas (ChatGPT). Write the verdict last, from the numbers on the page. **Chat** (settings `output: chat`, or the user asks): use the format below instead.


```
## Campaign retro: <name>, <start> to <end> (+7d tail)
Goal: <goal>   Target: <target or none set>   Result: <number or "not measured">

### Scorecard (campaign vs baseline)
| Channel | Metric | Baseline | Campaign | Change |
### Paid (only when Meta ads were readable; otherwise one line saying so)
| Campaign | Spend | Reach | Link clicks | LP views | Results | Cost/result |
### Timeline
| Date | What happened | Sessions | Key events |
### Facts
- ...
### Likely explanations
| Hypothesis | Confidence | What would confirm it |
### Repeat / Change / Stop
| Decision | Evidence | Owner | By |
### Tracking fixes
- <untagged links, split campaign names>
### Missing data
- ...
```

Feed repeat decisions into the next `campaign-plan`, tracking fixes into `utm-builder`.

## Never

- Never claim a post or ad caused a result when the timeline only shows they happened together.
- Never blame a person; name the process.
- Never edit, pause or change ads or posts from this skill. Read-only.
