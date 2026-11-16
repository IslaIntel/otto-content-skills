---
name: daily-pulse
description: A quick daily check of yesterday's posts through the Otto MCP, shown as a small dashboard - which posts are taking off, which stalled, what to remix today, and anything broken. Same look as the weekly review, scaled down to one day. Use when asked "how did yesterday's posts do", "daily pulse", "daily check-in", "how's my Instagram today", or before making today's content.
license: MIT
---

# Daily pulse

The weekly review, scaled down to one day: a five-minute overview, not a deep dive. It picks **within** your current plan (which posts to remix, which topics to rest, what broke) and never changes the plan. One day's results rise and fall together for reasons beyond content, so one day is never a reason to change strategy; that's the weekly review's job (`weekly-social-review`).

## 0. Setup

Before anything else (full rules: "How every skill talks to the user" in `otto-rules.md` (in this skill's folder)):
- **Settings**: read `brand/settings.md` (or what the assistant remembers). Don't ask what it already answers. Save new answers there (or to memory when there's no folder).
- **Account**: if the Otto connection has more than one business or more than one Instagram / Facebook account (`meta_page_list`), ask which, once.
- **Scope**: platforms the user named are the scope ("my Instagram" = Instagram only). Nothing named: use `default_platforms` from settings; with none saved, ask once with the connected platforms (`otto_list_connections`) as options plus "All connected", and save the answer. A platform in scope with no posts yesterday gets one line; out-of-scope platforms aren't mentioned.
- **Output**: visual by default (the dashboard below); chat if settings say `output: chat` or the user asks.
- Read-only: never call publish, schedule, delete, reply or hide tools.

## 1. Pull (platforms in scope only)

- **Instagram**: `meta_ig_list_media` (rowLimit 60, enough for the 4-week baseline at up to 2 posts a day; if the result is saved to a file, read the file). `meta_ig_media_insights` (batches of 25): `views, reach, likes, comments, shares, saved` for every post, plus `ig_reels_avg_watch_time, reels_skip_rate` for `mediaType: VIDEO` ids only (one image in the batch fails the whole call). `meta_ig_account_insights`, `metricType: time_series`, metric `reach`, last 8 days, `endDate` = today (end dates are exclusive). Record `profile.followersCount`.
- **Facebook**: `meta_page_posts` (rowLimit 60), then `meta_page_post_insights` for yesterday's posts and the baseline posts; `meta_page_insights` for the last 8 days for the daily chart (its `end_time` marks the end of the day) (`post_media_view` = views).
- **YouTube**: `youtube_list_recent_videos`, then `youtube_channel_analytics` with dimension `video`, metrics `views, averageViewPercentage, subscribersGained` for the last 2 days.
- **LinkedIn**: `linkedin_page_insights` for yesterday (page-level only; posts have no per-post numbers).

## 2. Baseline

**Same "usual" as the weekly review**, so the two never disagree. Per platform, the median reach (or views) of posts at least 3 days old from the **previous 28 days**, in this order: (1) the last weekly review's usual if the user attached its CSVs, the brand card states it, or `social-data/` has it; (2) otherwise from this pull. If the pull reaches back less than 28 days, say how many days the usual covers. Never compute it from only the last week or two: a short window makes a slow stretch look normal and every post look like it's taking off. Call it **B**. If a median is 0 (common for shares on small accounts), drop that signal and say so.

## 3. Judge

**Nothing posted yesterday?** Say so in one line ("Nothing went out on Sunday") and use the most recent day with posts as the early read, labelled with its day.

**Tiny platforms:** if a platform's usual is under 50, a post needs 100+ to count as taking off (shared rule).

**Yesterday's posts: early read.** Reach mostly settles in a day or two; under 20 hours old, mark it "young".

| Reach vs B | Early call (`status`) |
|---|---|
| 1.5x B or more | taking off (`winner`, label "Taking off") |
| 0.75x to 1.5x | on track (`keep`, label "On track") |
| under 0.75x | stalled (`stalled`) |

**Turned 3 days old today: formal call.** Taking off = 1.5x B or more. For any reel that stalled, run the `reel-diagnosis` steps and store the result in the post's `diagnosis`, so clicking it in the dashboard shows why.

**Totals first**: total views on the latest posting day's posts (the sum of each post's views; Instagram has no per-day views, so don't substitute account reach), per platform, vs the posting day before, as the headline (`hero`, `vsLabel` naming that day, e.g. "Friday's posts").

**Rolling 7 days** (as KPIs): posts, how many took off, median reach vs B, median skip rate, saves per 1,000 reach. **Followers**: today's total and the change since the last value saved on an **earlier day** (ignore values saved earlier today); say "net". No earlier value: show the total only.

## 4. Flag (breakage only)

Check only yesterday's posts and the ones that turned 3 days old today (older posts were already judged).
- A post over 24 hours old with reach under 20% of B, or a skip rate over 45%.
- A reel with no video: open its public page before flagging (the API sometimes returns `mediaUrl: null` for reels that still play).
- A day with no post when settings list a posting schedule.

## 5. Show it

- **Visual (default)**: fill `dashboard.html` in this folder following `dashboard-data.md`: `meta.title` "Daily pulse", one-day window, KPIs for the rolling 7 days, `posts` = yesterday's posts plus the ones that turned 3 days old today, `notes` = flags and "For today" (one remix, one topic to rest) with `notesTitle` "Flags and today". Use `status_label` "Taking off" / "On track" / "Stalled" / "Early read". No `plan`, `groups` or `decisions`. Artifact in claude.ai / Claude desktop; `social-data/reports/pulse-<YYYY-MM-DD>.html` opened in the browser in Claude Code / Cowork; canvas in ChatGPT.
- **Chat**: under 25 lines.

```markdown
# Daily pulse: <Weekday> <Mon D>
Followers: <n> (<+/-> since last check). Last 7 days: <k> of <m> posts took off; median reach <r> vs usual <B>.

| Post | Reach vs usual | Skip | Call | Why (stalled only) |

For today: remix <post, angle to change>. Rest <topic>. Flags: <flag with link, or "None">.
```

Name every post with its permalink. **No folder (claude.ai, ChatGPT):** offer the day's rows as a `posts.csv` download and say "attach this to the weekly review". With a folder, append the day's numbers to `social-data/posts.csv` and `social-data/account.csv` (same columns as `weekly-social-review`) when there's a folder, so the baseline keeps growing.
