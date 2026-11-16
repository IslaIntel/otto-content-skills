---
name: best-time-to-post
description: Work out when to post from your own history, comparing your posting times (converted to your timezone) with reach and views on the posts Otto pulls from Instagram, Facebook and YouTube, plus website visits by hour from GA4, and give an honest hypothesis to hold for 4 weeks. Use when asked "what time do my posts do best", "what hour should I post at", "what day is best for me", "does posting time matter for my account", or "set my posting schedule".
license: MIT
---

# Best time to post

Posting time usually matters less than what you post and how often. This skill checks whether it matters **for your account**, using the posts you've already made. It returns a slot plan you can keep, labelled clearly as a hypothesis when the sample is small, plus a 4-week hold so the next read means something. Read-only.

## 0. Setup

Follow the settings, scope and capability rules in `otto-rules.md` (in this skill's folder) ("How every skill talks to the user"). In short:
- Read `brand/settings.md` (or your memory of the user's Otto settings) first: workspace, accounts, default platforms, timezone, output mode. Ask only what's missing, as one multiple-choice question, and save the answers.
- Scope is the platforms the user names; otherwise the default from settings; otherwise ask once, listing connected platforms plus "All connected". A platform in scope with nothing in the window gets one line, never an empty table.

Then:
- **Timezone**: from settings; if missing, ask the person's timezone (or their audience's, if most customers live elsewhere) and save it. GA4 returns its property timezone in `metadata.timeZone`; use it if the person doesn't know.
- Ask how many posts a week they can actually keep up per platform. A schedule they won't follow is worse than none.

## 1. Pull

- **Instagram**: `meta_ig_list_media` (rowLimit 60). `timestamp` comes back in UTC (`+0000`): convert to the local timezone before bucketing. Then `meta_ig_media_insights` (batches of 25): `views, reach, shares`.
- **Facebook**: `meta_page_posts` (`createdTime`) + `meta_page_post_insights`.
- **LinkedIn**: `linkedin_page_posts` gives posting times only, with no per-post results, so LinkedIn can't be bucketed. Say so in one line.
- **YouTube**: `youtube_list_recent_videos` (publish time) + `youtube_channel_analytics` dimensions `["video"]`, metrics `["views"]`.
- **Website activity by hour (GA4, optional)**: `ga4_run_report` dimensions `["dayOfWeekName","hour"]`, metric `sessions`, last 8 weeks. This shows when your audience is online and on your site, in the property's timezone. Add a filter on `sessionDefaultChannelGroup` = `Organic Social` if there's enough social traffic (50+ sessions).
- Instagram's "most active times" for followers isn't available through the API (`online_followers` returns an error). If the person can screenshot it from the app (Professional dashboard > Total followers > Most active times), use it as one more input.

Use posts 7+ days old. `ok: false`: say so and continue.

## 2. Compute

1. **Normalise**: for each post, reach (Instagram) or views (Facebook `post_media_view`, YouTube) ÷ the platform median of the 10 posts around it (5 before, 5 after). This removes slow drift in account size, so a post isn't "good" just because it was recent.
2. **Bucket** by local day part: early (5-9), morning (9-12), midday (12-15), afternoon (15-18), evening (18-22), late (22-5). Also by weekday vs weekend. Hours are too fine for most accounts.
3. Per bucket: n, median normalised reach, and the share of posts above 1.0.

## 3. Read it honestly

| Situation | What to say |
|---|---|
| Fewer than 20 posts on the platform | Not enough data. Give a starting slot from GA4 peaks or the app's active-times screenshot, labelled as a guess. |
| Buckets with n < 5 | "too few to tell", whatever the median |
| Best bucket under 1.3x the worst bucket with n ≥ 5 | Timing doesn't visibly matter for you. Pick slots you can keep and focus on content. |
| Best bucket ≥ 1.3x, n ≥ 5, and 2/3 of its posts above 1.0 | A real lean. Make it the main slot. |
| All posts in one or two buckets | You've never tested other times: the data can't compare. Propose one test slot. |

Also check two things that often matter more than the hour: **gaps** (did reach drop after a week without posting?) and **stacking** (two posts within 3 hours on the same platform: did the second do worse?).

## 4. The plan

- **Main slots**: the best-supported bucket(s), at the cadence the person can keep (ask; no answer: keep their current cadence from the last 4 weeks and say so). Strongest post of the week goes in the best slot.
- **One test slot**: a bucket you have little data on, used for one post a week.
- **Hold for 4 weeks.** Change content freely, keep the times fixed. After 4 weeks rerun this skill: the test slot needs n ≥ 4 before comparing. Note the review date.

## 5. Output

**Visual (default):** fill `dashboard.html` in this folder (format in `dashboard-data.md`). `kpis`: posts analysed, timezone, best slot and weakest slot (each with its median and hours). `blocks`: a `heatmap` of median reach by day (rows) and time slot (columns), in the user's timezone, `null` where nothing was posted, `showValues: true`; `bars` by slot with the post count in each note; a `list` with the schedule to hold for 4 weeks. Show it as an artifact (claude.ai / Claude desktop), save and open it as `social-data/reports/best-time-to-post-<YYYY-MM-DD>.html` (Claude Code / Cowork), or a canvas (ChatGPT). Write the verdict last, from the numbers on the page. **Chat** (settings `output: chat`, or the user asks): use the format below instead.


```
## Best time to post: <business>, <timezone>
Posts analysed (platforms in scope only): IG <n> | FB <n> | ...   Window: <dates>

### When you've posted, and how it did
| Platform | Day part | n | Median vs neighbours | % above 1.0 | Read |
### Website activity (GA4, <timezone>)
Top 3 day/hour blocks: ...
### Verdict
<one of: timing matters (evidence) / timing doesn't visibly matter / not enough data>
### Schedule to hold until <date + 4 weeks>
| Platform | Days | Time | Role (main / test) |
### Bigger lever than timing (if any)
<e.g. 9-day gaps, two posts stacked in an hour>
```

Hand the schedule to `posting-plan` (or `post-queue` to line up posts against it). This skill never schedules posts itself.

## Never

- Never present a generic "best time" from the internet as the person's data.
- Never call a bucket with fewer than 5 posts a finding.
- Never schedule, move or publish anything from this skill.
