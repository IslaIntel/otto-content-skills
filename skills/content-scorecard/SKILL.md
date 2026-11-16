---
name: content-scorecard
description: Audit your recent posts (by default the last 30 days, or a longer range or post count you choose) on the Otto-connected platforms in scope (Instagram, Facebook, LinkedIn, YouTube), judged against your own median, to find which traits earn their keep and which are dead weight, ending in stop/keep/test lists, the next five posts, and an updated brand/winners.md. Use when asked to "audit my content", "which of my posts are working", "what should I quit posting", or "what should I double down on".
license: MIT
---

# Content audit

A once-a-month look at your recent posts, wide enough to see patterns a weekly review can't. By default it covers the last 30 days, however many posts that is; with only a handful, most patterns come out "too few to tell" and the audit says so. It answers three questions: which traits beat your own median, which keep losing, and what the next five posts should be. Read-only on every platform; the only file it writes is in your working directory.

## 0. Setup

Follow the settings, scope and capability rules in `otto-rules.md` (in this skill's folder) ("How every skill talks to the user"). In short:
- Read `brand/settings.md` (or your memory of the user's Otto settings) first: workspace, accounts, default platforms, output mode. Ask only what's missing, as one multiple-choice question, and save the answers.
- Scope is the platforms the user names; otherwise the default from settings; otherwise ask once, listing connected platforms plus "All connected". A platform in scope with no posts in the window gets one line, never an empty table. TikTok and X aren't available through Otto: ask for an export or screenshot if they matter.
- Read `brand/offer.md`, `brand/winners.md` and `social-data/posts.csv` if they exist (the CSV may already hold most of the numbers).

Skill-specific questions (ask together, multiple choice):
- **Window**: last 30 days (default), last 90 days, or the last N posts.
- **The account's job right now**: reach, followers, enquiries, or site visits. It sets the deciding metric in step 3. Ask it (multiple choice) unless settings have `account_goal`; save the answer. No answer: use reach and say so.

## 1. Pull

Every post in the chosen window per platform, skipping anything under 7 days old (still moving). For a long window, `meta_ig_list_media` stays at rowLimit 60 or less; page back if needed. Fewer than 5 posts on a platform is fine: report its numbers and mark its patterns "too few to tell".

- **Instagram**: `meta_ig_list_media` (rowLimit 60), then `meta_ig_media_insights` in batches of 25 with `views, reach, likes, comments, shares, saved, total_interactions, ig_reels_avg_watch_time, reels_skip_rate`. Never add `crossposted_views` or `facebook_views` (one non-crossposted reel fails the batch). `ig_reels_avg_watch_time` is ms; `reels_skip_rate` is already a percent. Request `ig_reels_avg_watch_time` and `reels_skip_rate` only for `mediaType: VIDEO` ids (one image in the batch fails the whole call).
- **Facebook Page**: `meta_page_posts`, then `meta_page_post_insights` in batches of 25.
- **LinkedIn Page**: `linkedin_page_posts` returns post text and dates only, no per-post numbers. Use `linkedin_page_insights` daily rows and match each post to the impressions in the 0-3 days after it; label those numbers approximate.
- **YouTube**: `youtube_channel_analytics` with dimensions `["video"]`, metrics `["views","averageViewPercentage","subscribersGained","shares","likes","comments"]`, sorted `-views`, for the window; `youtube_top_videos` for titles and links.
- **Site visits (if GA4 connected)**: `ga4_run_report`, dimensions `["sessionSource","landingPage"]`, metrics `["sessions","engagedSessions","keyEvents"]`, filtered to `sessionDefaultChannelGroup` = `Organic Social`. Visits by platform and page, not by post, unless links carry UTM tags (see `utm-builder`).

If a call returns `ok: false`, say which platform is missing and continue with the rest. Never fill gaps with estimates.

## 2. Tag every post

For each post record: platform, format (reel / carousel / image / video / text / short), length in seconds for video, **topic** (one of the account's 3-6 recurring subjects; use `brand/` pillars if they exist), **hook pattern** (first caption line or first spoken line, sorted with the buckets in `hook-patterns`), CTA type (none / comment / save / follow / link / DM), and whether a face appears in the first frame if you can tell from the caption or the person tells you. Unknown is fine; write "unknown", don't guess.

## 3. Compute, median first

1. **Per platform** median of: reach (or views), shares per 1k reach, saves per 1k reach, comments per 1k reach; for reels also skip rate and watch %; for YouTube average view % and subscribers gained per 1k views. Never sum views across platforms.
2. **Deciding metric** from the account's job:

| Job | Deciding metric |
|---|---|
| Reach / discovery | reach, then shares per 1k |
| Followers | YouTube subs per 1k views; on IG use account-level new follows on the post's day as a weak hint only |
| Enquiries / leads | comments + DMs the person reports, link clicks, GA4 key events from social |
| Trust / nurture | saves per 1k, average watch % |

3. **Trait multiple** = median of the deciding metric for posts with that trait ÷ the platform median. Report it like `1.8x (n=9)`.
4. Rules: a trait group under 5 posts is "too few to tell". A multiple between 0.8x and 1.25x is "no clear effect". One big outlier can't carry a trait: recompute without the top post and report if the multiple falls below 1.25x. **Check for time effects**: if a trait ran only or mostly (80%+ of its posts) in one stretch (a new series, a new posting cadence, a caption style change), compare it against the median of posts from that same stretch. A drop that hits every trait at once is a period effect (cadence, distribution), not a trait effect: say so. If a median is 0, drop that metric.

## 4. Decide

- **Keep**: traits at 1.25x+ with n ≥ 5 that still hold without the top post.
- **Stop**: traits at 0.8x or below with n ≥ 5, especially ones the account keeps making (n ≥ 8). Name them plainly.
- **Test**: traits that look strong on 2-4 posts, or a gap (a topic your audience asks about in comments or search that you haven't posted; `search-and-social` finds these). Design each with `hook-test`.
- **Next five posts**: each one cites the number that justifies it ("carousel + checklist hook, 2.1x saves, n=7"). Mix: three built on Keep traits, one test, one gap.

## 5. Update brand/winners.md

Append (don't overwrite) a dated section with the top 5 posts by the deciding metric: link, platform, date, the metric and its multiple vs median, traits, and one line on why it likely worked, marked as a hypothesis. Create the file if missing.

## 6. Output

Default is visual: fill `dashboard.html` in this folder (instructions in `dashboard-data.md`: lead with total views for the window (vs the window before, `vsLabel`) as a KPI, put the posts in `posts`, traits in `groups` with their `multiple` vs median, stop/keep/test in `plan` and the next five posts in `plan.next`) and show it as an artifact (claude.ai / Claude desktop), an HTML file opened in the browser (Claude Code / Cowork), or a canvas (ChatGPT). If settings say `output: chat` or the user asks for chat, give the same content as markdown in chat.

```
## Content audit: <business>, <first post date> to <last post date>
Posts reviewed (platforms in scope only): IG <n> | FB <n> | ...   Missing: <platforms + reason>
Account job: <job>  Deciding metric: <metric>

### Your medians
| Platform | Reach/views | Shares/1k | Saves/1k | Comments/1k | Skip % | Watch % |

### Traits vs your median
| Trait | Value | n | Multiple | Holds without top post? | Read |
(Read = keep / stop / test / too few to tell / no clear effect)

### Stop
- <trait>: <multiple>, n=<n>. <one line>
### Keep
- ...
### Test (max 2, each handed to hook-test)
- ...
### Next five posts
| # | Idea | Format | Hook pattern | Why (number) |

### What this data can't tell you
- <e.g. per-reel follows, TikTok, posts without UTM links>
```

End with one sentence: the single change that would move the deciding metric most.

## Never

- Never publish, schedule, delete or edit posts from this skill.
- Never present a pattern from fewer than 5 posts as a finding.
- Never compare to industry averages or another account's numbers.
- Never overwrite earlier entries in `brand/winners.md`.
